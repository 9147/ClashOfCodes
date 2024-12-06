from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

class DemoUser(models.Model):
    name = models.CharField(max_length=200)
    role_choices = [
        ('Team Member', 'Team Member'),
        ('Volunteer', 'Volunteer'),
        ('Judge', 'Judge'),
    ]
    id = models.CharField(max_length=200, unique=True, primary_key=True)
    role = models.CharField(max_length=20, choices=role_choices)
    team_name = models.CharField(max_length=200, blank=True, null=True)  # For team members

    # Food access permissions
    lunch1 = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch2 = models.BooleanField(default=False)

    lunch1_completed = models.BooleanField(default=False)
    dinner_completed = models.BooleanField(default=False)
    breakfast_completed = models.BooleanField(default=False)
    lunch2_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.dinner:
            self.breakfast = True
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CurrentFoodCheck(models.Model):
    food_choices = [
        ('lunch1', 'Lunch 1'),
        ('dinner', 'Dinner'),
        ('breakfast', 'Breakfast'),
        ('lunch2', 'Lunch 2'),
    ]
    current_food = models.CharField(max_length=10, choices=food_choices)

    def __str__(self):
        return f"Currently checking: {self.get_current_food_display()}"
