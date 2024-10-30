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