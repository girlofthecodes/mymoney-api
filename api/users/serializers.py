from users.models import User

#Imports for the validators
from rest_framework.serializers import ValidationError 
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import password_validation


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        validators = [UniqueValidator(queryset=User.objects.all(), message={'msg': 'El usuario ya existe. Introduzca un nombre de usuario distinto.'})]
    )
    email = serializers.EmailField(
        required=True, 
        validators = [UniqueValidator(queryset=User.objects.all(), message={'msg':'Este email ya existe. Introduzca un email distinto.'})]
    )
    
    class Meta:
        model = User
        fields = [
            'id', #Muestra el id del usuario
            'username',
            'email',
            'password',
            'is_active',
            'is_verified',
            'created_at',
            'updated_at',
        ]

        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        special_characters = "[~!@#$%^&*()_+{}\":;'[]-./=¿?<>]"


        if len(username) < 6: 
            raise ValidationError({"username":"El nombre de usuario debe tener un mínimo de 6 caracteres."})

        if len(username) > 20: 
            raise ValidationError({'username':'El nombre de usuario debe tener un máximo de 20 caracteres.'})

        if any(i.isspace() for i in username):
            raise ValidationError({'username':'El nombre de usuario no admite espacios.'})

        if any(i in special_characters for i in username): 
            raise ValidationError({'username':'El nombre de usuario no admite caracteres especiales.'})

        if any(i.isspace() for i in username):
            raise ValidationError({'username':'El nombre de usuario no admite espacios.'})

        if not any(i.isalpha() for i in password):
            raise ValidationError({'password':'La contraseña debe incluir al menos una letra.'})
        
        if not any(i.isupper() for i in password):
            raise ValidationError({'password':'La contraseña debe incluir al menos una letra mayúscula.'})
        
        if not any(i.isdigit() for i in password):
            raise ValidationError({'password':'La contraseña debe incluir al menos un dígito.'})
        
        if not any(i in special_characters for i in password): 
            raise ValidationError({'password':'La contraseña debe incluir al menos un caracter especial.'})

        if any(i.isspace() for i in password): 
            raise ValidationError({'password':'La contraseña no debe incluir espacios.'})

        if len(password) > 20:
            raise ValidationError({'password':'La contraseña debe tener un máximo 20 caracteres.'})
        
        if len(password) < 6:
            raise ValidationError({'password':'La contraseña debe tener un mínimo de 6 caracteres.'})
        
        return super(UserSignUpSerializer, self).validate(data)

        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSignUpSerializer, self).create(validated_data)


#Inicio de sesión
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=20)
    

    class Meta: 
        model = User
        fields = [
            'email', 
            'password',
            'is_active',
            'is_verified',
        ]
        

#Reseteo de contraseña.
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    newPassword = serializers.CharField(min_length=6, max_length=20, write_only=True)  
    confirmPassword = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True) #Token para comprobar que la contraseña es correcta
    uidb64 = serializers.CharField(min_length=1, write_only=True) #El id del usuario codificado en base 64

    class Meta:
        fields = ['newPassword', 'confirmPassword', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            newPassword = attrs.get('newPassword')
            confirmPassword = attrs.get('confirmPassword')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('El enlace de reinicio no es válido!!.')

            special_characters = "[~!@#$%^&*()_+{}\":;'[]-./=¿?<>]"

            if not any(i.isalpha() for i in newPassword):
                raise ValidationError({'newPassword': 'La contraseña debe contener al menos una letra.'})

            if not any(i.isupper() for i in newPassword):
                raise ValidationError({'newPassword': 'La contraseña debe incluir al menos una letra mayúscula'})

            if not any(i.isdigit() for i in newPassword):
                raise ValidationError({'newPassword': 'La contraseña debe incluir al menos un dígito'})

            if not any(i in special_characters for i in newPassword):
                raise ValidationError({'newPassword': 'La contraseña debe incluir al menos un caracter especial'})

            if any(i.isspace() for i in newPassword):
                raise ValidationError({'newPassword': 'La contraseña no debe incluir espacios'})

            if len(newPassword) > 20:
                raise ValidationError({'newPassword': 'La contraseña debe tener un máximo 20 caracteres'})

            if len(newPassword) < 6:
                raise ValidationError({'newPassword': 'La contraseña debe tener un mínimo de 6 caracteres'})

            if newPassword != confirmPassword:
                raise ValidationError({'confirmPassword': "Las contraseñas no coinciden."})

            if user.check_password(newPassword):  
                raise ValidationError({'newPassword': 'La nueva contraseña no puede ser la misma que la contraseña actual.'})

            password_validation.validate_password(newPassword, user)
        
            user.set_password(newPassword)
            user.is_active = True
            user.save()
            return user
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"El enlace de reinicio no es válido. Detalles: {str(e)}")
        except ValidationError as e:
            raise ValidationError(e.detail)
        except Exception as e:
            raise AuthenticationFailed(f"Error desconocido al procesar el enlace de reinicio: {str(e)}")
        

#Cambio de contraseña.
class ValidateCurrentPasswordASerializer(serializers.Serializer): 
    current_password = serializers.CharField(min_length=6, max_length=20)
    
    class Meta:
        fields = ['current_password']
        
    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise ValidationError({'msg': 'La contraseña actual no es correcta.'})
        return value



class ChangeNewPasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(min_length=6, max_length=20, write_only=True) 
    newPassword = serializers.CharField(min_length=6, max_length=20, write_only=True)  
    confirmPassword = serializers.CharField(min_length=6, max_length=20, write_only=True)
    
    class Meta:
        fields = [
            'currentPassword',
            'newPassword',
            'confirmPassword'
            ]

    def validate_currentPassword(self, value):
        if not self.context['request'].user.check_password(value):
            raise ValidationError({'currentPassword':'La contraseña actual no coincide.'})
        return value

    def validate(self, data):
        special_characters = "[~!@#$%^&*()_+{}\":;'[]-./=¿?<>]"

        if not any(i.isalpha() for i in data['newPassword']): 
            raise ValidationError({'newPassword':'La contraseña debe contener al menos una letra.'})
        
        if not any(i.isupper() for i in data['newPassword']):
            raise ValidationError({'newPassword':'La contraseña debe incluir al menos una letra mayúscula'})
        
        if not any(i.isdigit() for i in data['newPassword']):
            raise ValidationError({'newPassword':'La contraseña debe incluir al menos un dígito'})
        
        if not any(i in special_characters for i in data['newPassword']): 
            raise ValidationError({'newPassword':'La contraseña debe incluir al menos un caracter especial'})

        if any(i.isspace() for i in data['newPassword']): 
            raise ValidationError({'newPassword':'La contraseña no debe incluir espacios'})

        if len(data['newPassword']) > 20:
            raise ValidationError({'newPassword':'La contraseña debe tener un máximo 20 caracteres'})
        
        if len(data['newPassword']) < 6:
            raise ValidationError({'newPassword':'La contraseña debe tener un mínimo de 6 caracteres'})

        if data['newPassword'] != data['confirmPassword']:
            raise ValidationError({'confirmPassword':"Las contraseñas no coinciden."})

        if data['newPassword'] == data['currentPassword']: 
            raise ValidationError({'newPassword':'Esta contraseña ya ha sido usada. Prueba una diferente.'})
        
        password_validation.validate_password(data['newPassword'], self.context['request'].user)
        return data

#Logout
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages={
        'bad_token': ('Token inválido.')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

        
        