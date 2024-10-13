from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token_created_at = models.DateTimeField(default=timezone.now)


class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    problem_title = models.CharField(max_length=100)
    leader_name = models.CharField(max_length=100)
    leader_contact = models.CharField(max_length=12)
    member1_name = models.CharField(max_length=100)
    member2_name = models.CharField(max_length=100)
    member3_name = models.CharField(max_length=100)
    problem_description = models.TextField()
    problem_solution = models.TextField()
    problem_solution_file = models.FileField(upload_to='static/problem_solutions/')

    def __str__(self):
        return self.name
    

