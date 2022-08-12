from django.urls import path
from incomes import views

urlpatterns = [
    path('incomes/register/', views.IncomeRegisterView.as_view(),),  
    path('incomes/list/', views.IncomeListView.as_view(),),
    path('incomes/list/filter/', views.FilterIncomesListView.as_view(), ),
    path('incomes/update/<int:id>/', views.IncomeUpdateView.as_view(),),
    path('incomes/delete/<int:id>/', views.IncomeDeleteView.as_view(),),
]