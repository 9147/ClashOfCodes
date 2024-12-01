from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
import os
from django.utils.deconstruct import deconstructible
import random
from django.core.exceptions import ValidationError
import string
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=64, unique=True)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def is_token_expired(self):
        # Check if the token is older than 1 day
        expiration_time = self.token_created_at + timedelta(days=1)
        return timezone.now() > expiration_time

    def regenerate_token(self):
        # Regenerate token and reset timestamp
        self.token = get_random_string(length=64)  # Generate a new token
        self.token_created_at = timezone.now()
        self.save()



class Team(models.Model):
    name = models.CharField(max_length=300,unique=True)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teams')
    leader_contact = models.CharField(max_length=20)
    member1_name = models.CharField(max_length=100)
    member2_name = models.CharField(max_length=100)
    member3_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='City')
    college = models.CharField(max_length=100, default='College')
    state = models.CharField(max_length=100, default='State')
    country = models.CharField(max_length=100, default='Country')
    # problem_solution_file = models.FileField(upload_to='static/problem_solutions/')

    def __str__(self):
        return self.name
    
    
class submissiontime(models.Model):
    tag = models.CharField(max_length=300,primary_key=True)
    submission_time = models.DateTimeField()
    def __str__(self):
        return str(self.submission_time)
    

class contact(models.Model):
    email = models.EmailField()
    message = models.TextField()
    action_choice = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    action = models.CharField(max_length=10, choices=action_choice, default='Pending')
    def __str__(self):
        return self.message
    
@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        # Extract file extension
        ext = filename.split('.')[-1]
        
        # Get the team name and team ID
        team_name = instance.team.name
        team_id = instance.team.id

        # Create the new file name: teamname-teamid.extension
        filename = f'{team_name}-{team_id}.{ext}'
        
        # Return the full path to the file
        return os.path.join(self.sub_path, filename)

# Use this in your model field
class Problem(models.Model):
    title = models.CharField(max_length=1000)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    description = models.TextField()
    solution = models.TextField()
    domain = models.CharField(max_length=100,default='web')
    
    tracks_choice = [
        ('Digital', 'Digital'),
        ('3D','3D'),
    ]
    track = models.CharField(max_length=10, choices=tracks_choice, default='Digital')
    # solution pdf and ppt - use custom upload_to function
    solution_pdf = models.FileField(upload_to=UploadToPathAndRename('solutions/'), blank=True, null=True)
    status_choice = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    status = models.CharField(max_length=10, choices=status_choice, default='Pending')
    Referral = models.ForeignKey('ReferralCode', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    
class ladingPage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landing_page', primary_key=True)
    is_set = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class ReferralCode(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    Roles_choice = [
        ('Student', 'Student'),
        ('Faculty','Faculty'),
    ]
    role = models.CharField(max_length=10, choices=Roles_choice, default='Student')
    college = models.CharField(max_length=100, blank=True,default='KLS GIT')
    users = models.ManyToManyField(User, related_name='referral_groups')

    def __str__(self):
        return self.code

    @staticmethod
    def generate_code():
        # Generates a unique 6-character alphanumeric code
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not ReferralCode.objects.filter(code=code).exists():
                return code
    
    def save(self, *args, **kwargs):
        # Check if there are already 6 users in this group before saving
        if self.users.count() > 6:
            raise ValidationError("A ReferralGroup cannot have more than 6 users.")
        super().save(*args, **kwargs)

    def add_user(self, user):
        # Add the user to this ReferralGroup
        if self.users.count() >= 6:
            raise ValidationError("A ReferralGroup cannot have more than 6 users.")
        self.users.add(user)
        self.save()

    

