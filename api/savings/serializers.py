from savings.models import Saving
from users.models import User
from goals.models import Goal 

from rest_framework import serializers
from rest_framework.serializers import ValidationError


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email'
        ]

class GoalRegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Goal
        fields = [
            'id', 
            'goal_concept'
        ]

class SavingListSerializer(serializers.ModelSerializer):
    user = UserSignUpSerializer(read_only=True)
    goal = GoalRegisterSerializer(read_only=True)
    

    class Meta: 
        model = Saving
        fields = [
            'id',
            'user',
            'goal', 
            'saving_list', 
            'saving_date', 
            'saving_amount', 
            'saving_concept',
        ]

class SavingRegisterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Saving
        fields = [
            'user',
            'goal', 
            'id', 
            'saving_list', 
            'saving_date', 
            'saving_amount', 
            'saving_concept',
        ]
        extra_kwargs = {
            'saving_concept': {'required': False},
        }

    def validate(self, attrs): 
        user = attrs.get('user')
        goal = attrs.get('goal')

        if user.id != goal.user.id: 
            raise ValidationError({'msg':'Meta no perteneciente al usuario.'})

        return attrs

class SavingUpdateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Saving
        fields = [
            'user',
            'goal', 
            'id', 
            'saving_list', 
            'saving_date', 
            'saving_amount', 
            'saving_concept',
        ]
