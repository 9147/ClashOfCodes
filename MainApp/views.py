from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .serializers import ProblemSerializer, userSerializer
from .models import Payment, UserToken
from django.contrib.auth import authenticate, login, logout
from .models import Team, submissiontime, contact, submissiontime, Problem, ladingPage, ReferralCode
from django.template.loader import render_to_string
import json

# Create your views here.
def home(request):
    user = request.user
    context = {'user': user}
    # check if team of user is created
    # get landing page status
    if user.is_authenticated:
        landing_page, created = ladingPage.objects.get_or_create(user=user)
        if not created and landing_page.is_set:
            return redirect('MainApp:user')
    try:
        context['registration']= submissiontime.objects.get(tag='closingtime').submission_time.strftime("%B %d, %Y")
        context['idea']= submissiontime.objects.get(tag='idea').submission_time.strftime("%B %d, %Y")
        context['selection']= submissiontime.objects.get(tag='Top 40').submission_time.strftime("%B %d, %Y")
        context['hackathon']= submissiontime.objects.get(tag='hackathon').submission_time
        context['hackathon_end']= submissiontime.objects.get(tag='hackathon-end').submission_time
        team = Team.objects.get(leader=user.id)
        context['team'] = team
        problem = Problem.objects.filter(team=team)
        context['problem'] = problem
    except Exception as e:
        print(e)
        pass
    return render(request, "MainApp/index.html", context)


def register_user(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    
    if not email or email.strip() == '':
        return JsonResponse({'error': 'Email is required'}, status=404)
    
    user,created = User.objects.get_or_create(username=email,email=email,first_name=name)
    user.is_active = False
    user.save()
    
    # Generate a token for the user or regenerate if one exists
    user_token, _ = UserToken.objects.get_or_create(user=user)
    user_token.regenerate_token()  # Create or regenerate the token
    
    # Send the email (whether new user or existing user)
    domain = request.get_host()  # Get the domain dynamically
    protocol = 'https' if request.is_secure() else 'http'  # Check for HTTP/HTTPS

    mail_subject = 'Activate your account.'
    activation_link = f"{protocol}://{domain}/activate/{user.pk}/{user_token.token}/"

    # Render email content with context
   # Render HTML email content with context
    html_message = render_to_string('email_verification.html', {
        'user': user,
        'activation_link': activation_link,
    })

    # Create a plain text version as a fallback
    plain_message = f"""
    Hi {user.first_name or user.email},
    
    Thank you for registering for Clash of Codes. Please click the link below to verify your email and activate your account:
    
    Activation Link: {activation_link}
    
    If you did not create this account, please ignore this email.
    
    Regards,
    The Clash of Codes Team
    """

    # Create the email object using EmailMultiAlternatives
    email_message = EmailMultiAlternatives(
        subject=mail_subject,                 # Email subject
        body=plain_message,                   # Plain text body
        from_email='noreply@clashofcodes.in', # From email address
        to=[email],                           # Recipient's email
        reply_to=['contact@clashofcodes.in']  # Reply-to address
    )

    # Attach the HTML content as an alternative
    email_message.attach_alternative(html_message, "text/html")
    email_message.send(fail_silently=False)

    if created:
        return JsonResponse({'message': 'Verification link sent to your email'}, status=200)
    else:
        return JsonResponse({'message': 'Your account was deactivated and a new activation link was sent to your email'}, status=200)
    

def activate_user(request, uidb64, token):
    try:
        user = User.objects.get(pk=uidb64)
        user_token = UserToken.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, UserToken.DoesNotExist):
        return render(request,'MainApp/activation.html', {'message': 'Invalid activation link!'})

    if user_token.token == token:
        if not user_token.is_token_expired():  # Check if token is not expired
            if not user.is_active:
                user.is_active = True
                new_password = get_random_string(length=12)
                user.set_password(new_password)
                user.save()

                mail_subject = 'Your account has been activated'

                # Render the HTML email content using the template
                html_content = render_to_string('account_activation.html', {
                    'user': user,
                    'new_password': new_password,
                })

                # Create a plain text version as a fallback
                plain_text_content = f"""
                Hi {user.first_name},

                Your account has been successfully activated.

                Your new password is: {new_password}

                Please use this password to log in, and make sure to change your password after logging in for security reasons.

                If you did not request this activation or have any concerns, please contact our support team at contact@clashofcodes.in.

                Regards,
                Clash of Codes Team
                """

                # Create the email object using EmailMultiAlternatives
                email_message = EmailMultiAlternatives(
                    subject=mail_subject,                       # Email subject
                    body=plain_text_content,                    # Plain text body
                    from_email='noreply@clashofcodes.in',       # From email address
                    to=[user.email],                            # Recipient's email
                    reply_to=['contact@clashofcodes.in'],       # Reply-to email
                )

                # Attach the HTML content as an alternative
                email_message.attach_alternative(html_content, "text/html")

                # Send the email
                email_message.send(fail_silently=False)
                
                return render(request, 'MainApp/activation.html', {'message': 'Account activated successfully! Check your email for the new password.'})
            else:
                return render(request, 'MainApp/activation.html', {'message': 'Account already activated!'})
        else:
            return render(request, 'MainApp/activation.html', {'message': 'Activation link expired!'})
    else:
        return render(request, 'MainApp/activation.html', {'message': 'Invalid activation link!'})

    
def create_team(request):
    print(request.POST)
    
    # Get user
    user = User.objects.get(username=request.user.username)
    
    # Check if the user already has a team
    try:
        team = Team.objects.get(leader=user)
        if team:
            return render(request, 'MainApp/activation.html', {'message': 'You already have a team!'})
    except Team.DoesNotExist:
        pass  # Team does not exist, so we proceed

    # Serialize user data
    userserializer = userSerializer(user)

    # Gather team data from POST request
    data = {
        'name': request.POST.get('TeamName'),
        'leader_contact': request.POST.get('phoneno'),
        'member1_name': request.POST.get('member1'),
        'member2_name': request.POST.get('member2'),
        'member3_name': request.POST.get('member3'),
        'city': request.POST.get('city'),
        'state': request.POST.get('state'),
        'country': request.POST.get('country'),
        'college': request.POST.get('college'),
    }

    # Create and save the team
    try:
        team = Team.objects.create(
            name=data['name'],
            leader=user,
            leader_contact=data['leader_contact'],
            member1_name=data['member1_name'],
            member2_name=data['member2_name'],
            member3_name=data['member3_name'],
            city=data['city'],
            state=data['state'],
            country=data['country'],
            college=data['college']
        )
        team.save()

        # Email details
        mail_subject = 'Team Created Successfully'

        # Plain text email version
        plain_message = f"""
        Hi {user.first_name},

        Your team has been created successfully. You can now submit your idea.

        Team Name: {team.name}
        Leader Contact: {team.leader_contact}
        Member 1: {team.member1_name}
        Member 2: {team.member2_name}
        Member 3: {team.member3_name}

        Please join the WhatsApp group for further information:
        WhatsApp Link: https://chat.whatsapp.com/DOaKmPa64hNIhR5O77k1Qp

        Regards,
        Clash of Codes Team
        """

        # HTML email version
        html_message = render_to_string('team_creation_email.html', {
            'user': user,
            'team': team,
            'whatsapp_link': "https://chat.whatsapp.com/DOaKmPa64hNIhR5O77k1Qp"
        })

        # Create email with both plain text and HTML
        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=plain_message,
            from_email='noreply@clashofcodes.in',
            to=[user.email],
            reply_to=['contact@clashofcodes.in']
        )

        # Attach the HTML version
        email.attach_alternative(html_message, "text/html")

        # Send the email
        email.send(fail_silently=False)

    except Exception as e:
        return render(request, 'MainApp/activation.html', {'message': 'Team creation failed!'})

    # Redirect to home page after team creation
    return render(request, 'MainApp/activation.html', {'message': 'Team created successfully!'})

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            print("success")
            return JsonResponse({'data':'success'}, status=200)
        else:
            return JsonResponse(status=401)
    return JsonResponse(status=404)


def get_form_closing_time(request):
    closingtime = submissiontime.objects.get(tag='closingtime')
    return JsonResponse({'form_closing_time':closingtime.submission_time}, status=200)

def contactview(request):
    if request.method == 'POST':
        email = request.POST.get('email_address')
        message = request.POST.get('message')
        comment=contact.objects.create(email=email,message=message)
        return render(request,'MainApp/activation.html', {'message': 'Your message has been sent successfully!'})
    return render(request,'MainApp/activation.html',{'message':"message couldnt not be send!!"})

def referralValidation(request):
    if request.method == 'POST':
        referral_code = request.POST.get('referral_code')
        try:
            code = ReferralCode.objects.get(code=referral_code)
            return JsonResponse({'message': 'Referral code is valid!'}, status=200)
        except ReferralCode.DoesNotExist:
            return JsonResponse({'message': 'Referral code is invalid!'}, status=404)
        # check if users count is less than 6
        if code.users.count()<6:
            return JsonResponse({'message': 'Referral code is valid!'}, status=200)
        else:
            return JsonResponse({'message': 'The code is already used by 6 teams!'}, status=404)
    return JsonResponse({'message': 'Referral code could not be validated!'}, status=404)

def submission(request,track):
    if request.method == 'POST':
        problem_title = request.POST.get('problem-title')
        problem_statement = request.POST.get('problem-description')
        solution_description = request.POST.get('solution-description')
        domain = request.POST.get('domain')
        solution_file = request.FILES.get('Idea-ppt')  # Ensure to fetch the file from FILES, not POST
        referral_code = request.POST.get('referral_code').strip()

        code = None
        # Check if the referral code
        if referral_code:
            try:
                code = ReferralCode.objects.get(code=referral_code)
                if code.users.count()>6:
                    return render(request, 'MainApp/activation.html', {'message': 'The code is already used by 6 teams!'})
                code.users.add(request.user)
                code.save()
            except ReferralCode.DoesNotExist:
                return render(request, 'MainApp/activation.html', {'message': 'Referral code is invalid!'})

            # check if users count is less than 6
            
        
        try:
            team = Team.objects.get(leader=request.user)
        except Team.DoesNotExist:
            team = None


        if not team:
            return render(request, 'MainApp/activation.html', {'message': 'Team not found!'})

        # check if the problem is already present and just edit it
        try:
            problem = Problem.objects.get(team=team)
            problem.title = problem_title
            problem.description = problem_statement
            problem.solution = solution_description
            problem.domain = domain
            problem.solution_pdf = solution_file
            problem.save()
            return render(request, 'MainApp/activation.html', {'message': 'Problem statement updated successfully!'})
        except Problem.DoesNotExist:
            pass
        # Create the problem and attach the file
        problem = Problem.objects.create(
            title=problem_title,
            description=problem_statement,
            solution=solution_description,
            team=team,
            domain=domain,
            solution_pdf=solution_file,  # Assign the file to the model's FileField
            track = track,
            Referral=code
        )
        problem.save()

        return render(request, 'MainApp/activation.html', {'message': 'Problem statement submitted successfully!'})
    
    # check if the user already has made submission
    try:
        team = Team.objects.get(leader=request.user)
        problem = Problem.objects.get(team=team)
        problem = ProblemSerializer(problem)
        return render(request, 'MainApp/submission.html', {"problem": problem.data,"track":track})
    except Problem.DoesNotExist:
        return render(request, 'MainApp/submission.html',{'track':track})

def logout_user(request):
    logout(request)
    return render(request, 'MainApp/activation.html', {'message': 'Logout successful!'})

def user_view(request):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('MainApp:login')
    # check if langing page is set
    landing_page, created = ladingPage.objects.get_or_create(user=request.user)
    # check if user has team
    print(landing_page.is_set)
    # get referral code
    context = {'landing_page': landing_page.is_set}
    try:
        team = Team.objects.get(leader=request.user)
        context['team'] =  team
    except Team.DoesNotExist:
        context['team'] = None
        context['message'] = "1"
        return render(request, 'MainApp/user.html', context)
    # check if user has submitted problem statement
    try:
        problem = Problem.objects.get(team=team)
        context['problem'] = problem
        if problem.Referral:
            context['referral'] = problem.Referral.code
            context['referral_diff'] = 6 - problem.Referral.users.count()
    except Problem.DoesNotExist:
        context['problem'] = None
        context['message'] = "2"
        return render(request, 'MainApp/user.html', context)
    # check if payment is completed
    try:
        payment = Payment.objects.get(user=request.user)
        context['payment'] = payment
    except Payment.DoesNotExist:
        context['payment'] = None
        return render(request, 'MainApp/user.html', context)
    return render(request, 'MainApp/user.html', context)

def update_landing_page(request):
    if request.method == 'POST':
        is_set = request.POST.get('is_set')
        is_set = True if is_set.lower() == 'true' else False
        user = request.user
        landing_page = ladingPage.objects.get(user=user)
        landing_page.is_set = is_set
        landing_page.save()
        print(landing_page.is_set)
        return JsonResponse({'message': 'Landing page updated successfully!'}, status=200)
    return JsonResponse({'message': 'Landing page could not be updated!'}, status=404)


def generateReferralCode(request):
    if request.method == 'POST':
        college = request.POST.get('college')
        role = request.POST.get('role')
        print("value: ",college,role)
        code = ReferralCode.objects.create(code=ReferralCode.generate_code(), college=college,role=role)
        code.save()
        return JsonResponse({'message': 'Referral code generated successfully!','referral_code':code.code}, status=200)
    else:
        return render(request,'MainApp/referralCode.html')
    
def discount(request):
    return render(request,'MainApp/discount.html')


def make_payment(request):
    if request.method == 'POST':
        user = request.user
        user = User.objects.get(username=user.username)
        utr_number = request.POST.get('transaction_id')
        payment_screenshot = request.FILES.get('screenshot')
        if not utr_number or not payment_screenshot:
            return JsonResponse({'message': 'Please provide all the details!','status':"fail"}, status=404)
        # if user has already made payment
        try:
            payment = user.payment
            payment.utr_number = utr_number
            payment.payment_screenshot = payment_screenshot
            payment.save()
            return JsonResponse({'message': 'Payment details updated successfully!','status':"success"}, status=200)
        except:
            payment = Payment.objects.create(user=user,utr_number=utr_number,payment_screenshot=payment_screenshot)
            payment.save()
            return JsonResponse({'message': 'Payment details added successfully!','status':"success"}, status=200)
    return JsonResponse({'message': 'Payment details could not be added!','status':"fail"}, status=404)


def save_github_url(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        github_url = data.get('githubUrl')
        # save url in problem model
        try:
            user = request.user
            team = Team.objects.get(leader=user)
            problem = Problem.objects.get(team=team)
            problem.github_link = github_url
            problem.save()
        except:
            return JsonResponse({'message': 'Error saving GitHub URL!'}, status=400)
        return JsonResponse({'message': 'GitHub URL successfully added!'}, status=200)
    return JsonResponse({'message': 'Invalid request!'}, status=400)
