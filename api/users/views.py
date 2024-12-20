from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from users.serializers import UserSignUpSerializer, UserLoginSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, ValidateCurrentPasswordASerializer, ChangeNewPasswordSerializer, UserLogoutSerializer
from users.models import User
from .utils import Util
import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


#Generador automático de token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#Registro de usuario
class UserSignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request): 
        try: 
            serializer = UserSignUpSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save() 
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
            email_body = '¡Hola '+ user.username +'!\nUsa el siguiente link para verificar tu correo electrónico: \n' + absurl
            data = {
                'email_body': email_body, 
                'to_email': user.email, 
                'email_subject': 'Verificación de email.'
            }
            
            if Util.send_email(data):
                print("Se envio el correo")
            else: 
                print("No se envio el correo") 
            
            
            return Response(user_data, status=status.HTTP_201_CREATED)
        except Exception as e :
            print(f"Ocurrió un error: {e}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Verificación de registro mediante un email
class VerifyEmail(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'msg':'Activado exitosamente.'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError: 
            return Response({'msg':'El link de activación expiró.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError: 
            return Response({'msg':'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

#Login
class UserLoginView(APIView): 
    permission_classes = [permissions.AllowAny]
    def post(self, request): 
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']  
        password = serializer.data['password']
        try: 
            user = User.objects.get(email=email)
        except: 
            return Response({'msg':'Email y/o contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)

        #Autentica el usuario    
        user_auth = authenticate(email=email, password=password)   
        if user_auth: 
            user_auth.login_attempts = 0
            user_auth.save()
            tokens = get_tokens_for_user(user_auth)
            data = {
                'msg': 'Inicio de sesión exitoso.',
                'tokens': tokens
            }
            return Response(data, status=status.HTTP_200_OK)  
        
        user = User.objects.get(email=email)
        
        if not user.is_verified: 
                raise AuthenticationFailed({'msg':'Tu cuenta no ha sido activada, verifica tu email.'})

        #No autenticacion del usuario
        if user.login_attempts < 3: 
            while not user_auth: 
                user.login_attempts += 1
                user.save()    
                raise AuthenticationFailed({'msg':'Email y/o contraseña incorrecta.'})
        else: 
            user.is_active = False
            user.save()
            raise AuthenticationFailed({'msg':'La cuenta se ha bloqueado. Resetea tu contraseña.'})


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user 
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = 'localhost:5173'
            #current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://'+current_site + relativeLink
            email_body = '¡Hola '+ user.username +'!\nUsa el enlace a continuación para restablecer tu contraseña:\n' +absurl
            data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Restablece tu contraseña'}
            Util.send_email(data)
            print("Se envio el email")
        return Response({'success': 'Te hemos enviado un enlace para restablecer tu contraseña.'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'msg': 'El token no es válido, solicita uno nuevo.'}, status=status.HTTP_401_UNAUTHORIZED)

            return  Response({'msg':'Credenciales válidas', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'msg': 'El ID de usuario no es válido.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Restablecimiento de contraseña exitoso.'}, status=status.HTTP_200_OK)

#Validacion de la contraseña para permitir su cambio 
class ValidateCurrentPasswordAPIView(generics.GenericAPIView): 
    serializer_class = ValidateCurrentPasswordASerializer
    permission_classes=[IsAuthenticated, ]
    
    def post(self, request): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Contraseña actual válida. Ahora puedes cambiar tu contraseña.'}, status=status.HTTP_200_OK)

#Cambio de contraseña
class ChangeNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangeNewPasswordSerializer
    permission_classes=[IsAuthenticated, ]

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['newPassword'])
        request.user.save()
        data = {
            'msg':'Cambio de contraseña exitoso.'
        }
        return Response(data, status=status.HTTP_200_OK)

#Logout
class UserLogoutAPIView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes=[IsAuthenticated, ]
    def post(self, request): 
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()    
        data = {
            'msg':'Logout exitoso.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

