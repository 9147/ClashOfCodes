from rest_framework import serializers
from .models import Team, contact
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']

class TeamSerializer(serializers.ModelSerializer):
    leader = userSerializer()
    name = serializers.CharField(required=True)
    leader_contact = serializers.CharField(required=True)
    member1_name = serializers.CharField(required=True)
    member2_name = serializers.CharField(required=True)
    member3_name = serializers.CharField(required=True)

    class Meta:
        model = Team
        fields = '__all__'

    def create(self, validated_data):
        leader_data = validated_data.pop('leader')
        print("leader_data",leader_data)
        leader_id = leader_data.get('id')
        leader = User.objects.get(leader_id)
        if not leader:
            raise serializers.ValidationError("Leader not found")
        
        team = Team.objects.create(leader=leader, **validated_data)
        return team
    
class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = '__all__'