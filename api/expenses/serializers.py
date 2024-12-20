from os import access
from re import T
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from expenses.models import Expense
from accounts.models import Account 
from labels.models import Label
from users.models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email'
        ]
    
        
class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 
            'account_name',
        ]

class LabelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = [
            'id',
            'label_name'
        ]

class ExpenseRegisterSerializer(serializers.ModelSerializer):
    expenseDescription = serializers.CharField(source='expense_description'); 
    expenseDate = serializers.DateField(source='expense_date', required=False);
    expenseAmount = serializers.DecimalField(source='expense_amount', max_digits=10, decimal_places=2); 
    class Meta: 
        model = Expense
        fields = [
            'id',
            'user',
            'account',
            'label',
            'expenseDescription',
            'expenseDate', 
            'expenseAmount', 

        ]
        extra_kwargs = {
            'expenseDescription': {'required': False},
            'expenseDate': {'required': False},
        }


    def validate(self, attrs): 
        account = attrs.get('account', '')
        label = attrs.get('label', '')
        user = attrs.get('user', '')

        if user.id != account.user.id:
            raise ValidationError({'msg':'Cuenta no perteneciente al usuario.'})

        if user.id != label.user.id:
            raise ValidationError({'msg':'Etiqueta no perteneciente al usuario.'})

        if label.status_delete: 
            label.status_delete = True
            raise ValidationError({'msg':'La etiqueta seleccionada no existe.'})

        if account.status_delete: 
            account.status_delete = True
            raise ValidationError({'msg':'La cuenta seleccionada no existe.'})

        if attrs.get('expense_amount')  > account.current_balance: 
            raise ValidationError({'msg':'El gasto es mayor al monto que tiene disponible en la cuenta seleccionada.'})

        account.current_balance = account.current_balance - attrs.get('expense_amount')
        account.save()

        return attrs


class ExpenseListSerializer(serializers.ModelSerializer): 
    user = UserSignUpSerializer(read_only=True) 
    account = AccountRegisterSerializer(read_only=True) 
    label = LabelRegisterSerializer(read_only=True)
    expenseDescription = serializers.CharField(source='expense_description'); 
    expenseDate = serializers.DateField(source='expense_date', required=False);
    expenseAmount = serializers.DecimalField(source='expense_amount', max_digits=10, decimal_places=2); 

    class Meta: 
        model = Expense
        fields = [
            'id',
            'user',
            'account',
            'label',
            'expenseDescription',
            'expenseDate', 
            'expenseAmount', 
        ]
        

class ExpenseUpdateSerializer(serializers.ModelSerializer): 
    expenseDescription = serializers.CharField(source='expense_description'); 
    expenseDate = serializers.DateField(source='expense_date', required=False);
    expenseAmount = serializers.DecimalField(source='expense_amount', max_digits=10, decimal_places=2); 
    class Meta: 
        model = Expense
        fields = [
            'id',
            'user',
            'account',
            'label',
            'expenseDescription',
            'expenseDate', 
            'expenseAmount',
        ]
        read_only_fields = ['account', 'label',]
