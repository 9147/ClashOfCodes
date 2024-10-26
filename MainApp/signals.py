import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ReferralCode, Problem
from django.db.models.signals import post_delete, post_save

def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not ReferralCode.objects.filter(code=code).exists():
            return code

@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    if created:
        # Generate and assign a referral code to the new user
        ReferralCode.objects.create(user=instance, code=generate_unique_code())

# Signal to handle referral count decrease on Problem deletion
@receiver(post_delete, sender=Problem)
def decrement_referral_count_on_problem_delete(sender, instance, **kwargs):
    if instance.Referral:
        # Decrease referral count in the associated ReferralCode
        referral_code = instance.Referral
        referral_code.referral_count = max(0, referral_code.referral_count - 1)  # Ensure count doesn't go below zero
        referral_code.save()