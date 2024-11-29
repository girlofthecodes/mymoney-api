from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import Account


class AccountRegisterSerializer(serializers.ModelSerializer):
    accountName = serializers.CharField(source='account_name')  
    accountType = serializers.CharField(source='account_type')  
    accountNumber = serializers.CharField(source='account_number')  
    currentBalance = serializers.DecimalField(source='current_balance', max_digits=10, decimal_places=2)  
    dueDate = serializers.DateField(source='due_date', required=False)  

    class Meta:
        model = Account
        fields = [
            'user',
            'id', 
            'accountName',  
            'accountType',  
            'accountNumber',  
            'currentBalance',  
            'dueDate',  
        ]
        extra_kwargs = {
            'accountName': {'required': False},  
            'accountNumber': {'required': False},  
        }
    
    def validate(self, data): 
        account_type = data.get('accountType', None)
        account_number = data.get('accountNumber', None)

        if account_type == "Ahorro": 
            if len(account_number) != 16 or any(i.isalpha() for i in account_number): 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        if account_type == "Nómina": 
            if len(account_number) != 16 or any(i.isalpha() for i in account_number): 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        if account_type == "Efectivo": 
            if account_number is None: 
                return data 
            raise ValidationError({'msg':f'La cuenta {account_type} no necesita número de cuenta.'})
        if account_type == "Crédito": 
            if len(account_number) != 16 or any(i.isalpha() for i in account_number): 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        if account_type == "Wallet": 
            if len(account_number) != 128: 
                raise ValidationError({'msg':'El número de cuenta debe contener 128 dígitos.'})
        if account_type == "Departamental":
            if account_number is None:
                raise ValidationError({'msg': 'El número de cuenta no puede estar vacío para cuentas Departamentales.'})

            if len(account_number) != 16:
                raise ValidationError({'msg': 'El número de cuenta debe contener 16 dígitos para cuentas Departamentales.'})
            
            if not any(i.isalpha() for i in account_number):  
                raise ValidationError({'msg': 'El número de cuenta debe contener solo caracteres alfanuméricos.'})
            
        if account_type == "Vales": 
            if len(account_number) != 16 or any(i.isalpha() for i in account_number): 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        
        return data 
