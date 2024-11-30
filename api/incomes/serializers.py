from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users.models import User
from accounts.models import Account
from labels.models import Label
from incomes.models import Income


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

class IncomeRegisterSerializer(serializers.ModelSerializer): 
    incomeDate = serializers.DateField(source='income_date', required=False)  
    incomeAmount = serializers.DecimalField( source='income_amount', max_digits=10, decimal_places=2) 
    incomeDescription = serializers.CharField(source='income_description', required=False)
    class Meta: 
        model = Income
        fields = [
            'id',
            'user',
            'account',
            'label',
            'incomeDate',
            'incomeAmount',
            'incomeDescription',
        ]
        extra_kwargs = {
            'incomeDescription': {'required': False}
        }

    def validate(self, attrs): 
        account = attrs.get('account')
        label = attrs.get('label')
        user = attrs.get('user')


        if user.id != account.user.id:
            raise ValidationError({'msg':'Cuenta no perteneciente al usuario'})

        elif user.id != label.user.id:
            raise ValidationError({'msg':'Etiqueta no perteneciente al usuario'})
        elif label.status_delete: 
            label.status_delete = True
            raise ValidationError({'msg':'La etiqueta seleccionada no existe.'})

        elif account.status_delete: 
            account.status_delete = True
            raise ValidationError({'msg':'La cuenta seleccionada no existe.'})
        else: 
            account.current_balance = account.current_balance + attrs.get('income_amount')
            account.save()

        return attrs

class IncomeListSerializer(serializers.ModelSerializer): 
    user = UserSignUpSerializer(read_only=True) 
    account = AccountRegisterSerializer(read_only=True) 
    label = LabelRegisterSerializer(read_only=True)
    incomeDate = serializers.DateField(source='income_date', read_only=True)  
    incomeAmount = serializers.DecimalField( source='income_amount', max_digits=10, decimal_places=2, read_only=True) 
    incomeDescription = serializers.CharField(source='income_description', required=False, read_only=True)

    class Meta: 
        model = Income
        fields = [
            'id',
            'user',  
            'account',
            'label',
            'incomeDate',
            'incomeAmount',
            'incomeDescription'
        ]

class IncomeUpdateSerializer(serializers.ModelSerializer): 
    incomeDate = serializers.DateField(source='income_date', required=False)  
    incomeAmount = serializers.DecimalField( source='income_amount', max_digits=10, decimal_places=2) 
    incomeDescription = serializers.CharField(source='income_description', required=False)
    
    class Meta: 
        model = Income
        fields = [
            'id',
            'user',  
            'account',
            'label',
            'incomeDate',
            'incomeAmount',
            'incomeDescription',
        ]
        read_only_fields = ['account', 'label',]
