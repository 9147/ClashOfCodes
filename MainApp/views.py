from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .serializers import TeamSerializer, userSerializer
from .models import UserToken
from django.contrib.auth import authenticate, login
from .models import Team, submissiontime, contact, submissiontime, Problem
from django.template.loader import render_to_string
from django.http import FileResponse, Http404
from django.conf import settings
import os

# Create your views here.
def home(request):
    user = request.user
    context = {'user': user}
    # check if team of user is created

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
    
    try:
        user = User.objects.get(username=email)
        user.is_active = False  # Deactivate the account
        user.save()
        created = False
    except User.DoesNotExist:
        user = User.objects.create(username=email, email=email, first_name=name)
        user.is_active = False  # Deactivate the account
        user.save()
        created = True
    
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
        return JsonResponse({'message': 'Verification link sent to your email'}, status=201)
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
            member3_name=data['member3_name']
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


def submission(request):
    if request.method == 'POST':
        problem_title = request.POST.get('problem-title')
        problem_statement = request.POST.get('problem-description')
        solution_description = request.POST.get('solution-description')
        solution_file = request.FILES.get('Idea-ppt')  # Ensure to fetch the file from FILES, not POST
        try:
            team = Team.objects.get(leader=request.user)
        except Team.DoesNotExist:
            team = None

        if not team:
            return render(request, 'MainApp/activation.html', {'message': 'Team not found!'})

        # Create the problem and attach the file
        problem = Problem.objects.create(
            title=problem_title,
            description=problem_statement,
            solution=solution_description,
            team=team,
            solution_pdf=solution_file  # Assign the file to the model's FileField
        )
        problem.save()

        return render(request, 'MainApp/activation.html', {'message': 'Problem statement submitted successfully!'})
    
    return render(request, 'MainApp/submission.html')

