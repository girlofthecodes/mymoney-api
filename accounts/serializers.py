from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import Account


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'user',
            'id', 
            'account_name',
            'account_type',
            'account_number',
            'current_balance',
            'due_date',
        ]
        extra_kwargs = {
            'account_name': {'required': False},
            'account_number': {'required': False},
        }
    
    def validate(self, data): 
        account_type = data.get('account_type', None)
        account_number = data.get('account_number', None)

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
        if account_type == "Departamental" or not any(i.isalpha() for i in account_number): #Se le agrego not a la sentencia para probar que solo acepte caracteres alfanumericos
            if len(account_number) != 16: 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        if account_type == "Vales": 
            if len(account_number) != 16 or any(i.isalpha() for i in account_number): 
                raise ValidationError({'msg':'El número de cuenta debe contener 16 dígitos.'})
        
        return data 
