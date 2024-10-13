from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'problem_title', 'member1_name', 'member2_name', 'member3_name', 'problem_description', 'problem_solution', 'problem_solution_file']
