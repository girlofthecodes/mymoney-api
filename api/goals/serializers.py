from goals.models import Goal

from rest_framework import serializers

from rest_framework.serializers import ValidationError


class GoalRegisterSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Goal
        fields = [
            'user', 
            'id', 
            'goal_concept',
            'start_date', 
            'due_date', 
            'goal_amount', 
            'goal_period', 
            'goal_total', 
            'goal_color',
        ]
        extra_kwargs = {
            'goal_total': {'required': False},
        }
    
    def validate(self, data): 
        goal_total = data.get('goal_total')
        
        if data['due_date'] < data['start_date']:
            raise ValidationError({'msg':'La fecha final debe ser mayor a la fecha inicial.'})


        if data['goal_period'] == "Diario": 
            goal_total = data['due_date'] - data['start_date']
            goal_total = goal_total.days * data['goal_amount']
            data['goal_total'] = goal_total
            

        if data['goal_period'] == 'Semanal':
            goal_total = data['due_date'] - data['start_date']
            goal_total = (goal_total.days) / 7
            goal_total = round(goal_total) * (data['goal_amount'])
            data['goal_total'] = goal_total


        if data['goal_period'] == 'Quincenal':
            goal_total = data['due_date'] - data['start_date']
            goal_total = (goal_total.days) / 15
            goal_total = round(goal_total) * (data['goal_amount'])
            data['goal_total'] = goal_total


        if data['goal_period'] == 'Mensual':
            goal_total = data['due_date'] - data['start_date']
            goal_total = (goal_total.days) / 30
            goal_total = round(goal_total) * (data['goal_amount'])
            data['goal_total'] = goal_total


        return data 

class GoalListSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Goal
        fields = [
            'user', 
            'id', 
            'goal_concept',
            'start_date', 
            'due_date', 
            'goal_amount', 
            'goal_period', 
            'goal_total', 
            'goal_color',
        ]
        
