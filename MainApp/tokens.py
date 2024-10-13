from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils import timezone

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include user PK, active status, and timestamp in the hash
        return f"{user.pk}{user.is_active}{timestamp}"

    def check_token(self, user, token):
        """
        Override the check_token method to add token expiration handling.
        """
        # Use Django's default token validation logic first
        if not super().check_token(user, token):
            return False

        # Define token expiration period (e.g., 1 day)
        expiration_days = 1
        current_time = timezone.now()

        # Ensure that the user's last login or date joined is timezone-aware
        user_last_login_or_joined = user.last_login or user.date_joined
        if timezone.is_naive(user_last_login_or_joined):
            user_last_login_or_joined = timezone.make_aware(user_last_login_or_joined, timezone.get_current_timezone())

        # Check if the token is expired
        if current_time > user_last_login_or_joined + timedelta(days=expiration_days):
            return False  # Token is expired

        return True

account_activation_token = CustomTokenGenerator()
