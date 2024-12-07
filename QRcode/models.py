from django.db import models
import random
import string

def generate_unique_code():
    """Generate a 16-character unique code."""
    characters = string.ascii_letters + string.digits
    while True:
        unique_code = ''.join(random.choices(characters, k=16))
        if not DemoUser.objects.filter(unique_code=unique_code).exists():
            return unique_code

class DemoUser(models.Model):
    name = models.CharField(max_length=200)
    role_choices = [
        ('Team Member', 'Team Member'),
        ('Volunteer', 'Volunteer'),
        ('Judge', 'Judge'),
    ]
    id = models.CharField(max_length=10, primary_key=True, editable=False)
    unique_code = models.CharField(max_length=16, unique=True, editable=False)
    role = models.CharField(max_length=20, choices=role_choices)
    team_name = models.CharField(max_length=200, blank=True, null=True)

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

        if not self.id:
            # Generate ID
            last_id = DemoUser.objects.order_by('id').last()
            if last_id:
                last_id_number = int(last_id.id)
                new_id = str(last_id_number + 1).zfill(3)  # Zero-fill to 5 digits
            else:
                new_id = "001"  # Start from 00001
            self.id = new_id

        if not self.unique_code:
            # Generate 16-character unique code
            self.unique_code = generate_unique_code()
        
        super(DemoUser,self).save(*args, **kwargs)


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
