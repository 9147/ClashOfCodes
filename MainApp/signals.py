import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ReferralCode

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