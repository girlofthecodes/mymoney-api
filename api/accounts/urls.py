from django.urls import path
from accounts import views

urlpatterns = [
    path('accounts/register/', views.AccountRegisterView.as_view(),),
    path('accounts/list/', views.AccountsListView.as_view(),),
    path('accounts/list/<id>/', views.AccountIDListView.as_view(),), #Filtra por id
    path('accounts/update/<id>/', views.AccountUpdateView.as_view(),),
    path('accounts/delete/<id>/', views.AccountDeleteView.as_view(),),
]