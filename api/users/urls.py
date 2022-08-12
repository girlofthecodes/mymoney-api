from django.urls import path
from users import views

urlpatterns = [
    path('auth/signup/', views.UserSignUpView.as_view(), ),
    path('auth/email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('auth/login/',views.UserLoginView.as_view(),),

    #Reseteo de contraseña.
    path('auth/request-reset/', views.RequestPasswordResetEmail.as_view(),name="request-reset"), #Manda al email que quiere restablecer la contraseña
    path('auth/password-reset-confirm/<uidb64>/<token>/',views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), #A traves del link, se mandaran lque se ha validado las credenciales y se enviara el token
    path('auth/password-reset-complete/', views.SetNewPasswordAPIView.as_view(),name='password-reset-complete'), #Pide los datos proporcionados en la url anterior, como uidb64, token y password

    #Cambio de contraseña.
    path('auth/password-change/', views.ChangeNewPasswordAPIView.as_view(), name="password-change"), 

    #Logout
    path('auth/logout/',views.UserLogoutAPIView.as_view(),),
]

