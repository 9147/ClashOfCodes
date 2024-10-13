from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes,permission_classes,authentication_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from .tokens import account_activation_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.crypto import get_random_string
from .serializers import TeamSerializer
from .models import UserToken, Team
from django.utils import timezone
from datetime import timedelta




# Create your views here.
def home(request):
    return HttpResponse("Hello World")


class RegisterThrottle(UserRateThrottle):
    rate = '5/hour'

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([RegisterThrottle])
def register_user(request):
    email = request.data.get('email')
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user, created = User.objects.get_or_create(username=email, email=email)
    
    # If the user already exists but is trying to register again, deactivate their account
    if not created:
        user.is_active = False  # Deactivate the account
        user.save()

    # Update token timestamp
    user_token, _ = UserToken.objects.get_or_create(user=user)
    user_token.token_created_at = timezone.now()
    user_token.save()

    # Send the email (whether new user or existing user)
    domain = request.get_host()  # Get the domain dynamically
    protocol = 'https' if request.is_secure() else 'http'  # Check for HTTP/HTTPS

    mail_subject = 'Activate your account.'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    
    # Construct the activation link
    activation_link = f"{protocol}://{domain}/activate/{uid}/{token}/"

    # Render email content with context
    message = render_to_string('email_verification.html', {
        'user': user,
        'activation_link': activation_link,  # Pass the generated activation link
    })

    # Create and send an email message as HTML
    email_message = EmailMessage(
        mail_subject,
        message,
        'your_email@gmail.com',  # From email
        [email],                 # To email
    )
    email_message.content_subtype = 'html'  # Set content type to HTML
    email_message.send()

    if created:
        return Response({'message': 'Verification link sent to your email'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Your account was deactivated and a new activation link was sent to your email'}, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, uidb64, token):
    try:
        # Decode the uid
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user_token = UserToken.objects.get(user=user)
        
        # Check if the token was created after the last token creation time
        if account_activation_token.check_token(user, token) and timezone.now() < user_token.token_created_at + timedelta(days=1):
            # Activate the user if the token is valid and not expired
            user.is_active = True
            
            # Generate a new random password
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            # Send the new password via email
            mail_subject = 'Your new password'
            message = f"Hi {user.email},\n\nYour account has been activated. Your new password is: {new_password}\n\nPlease use this password to log in."
            send_mail(mail_subject, message, 'your_email@gmail.com', [user.email])

            return redirect('https://google.com')   # Redirect to login page after successful activation
        else:
            return Response({'error': 'Activation link is invalid or expired!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])  # Use token authentication for this specific view
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the team details
        serializer.save()
        return Response({'message': 'Team created successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



