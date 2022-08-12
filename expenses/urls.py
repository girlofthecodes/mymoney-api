from django.urls import path
from expenses import views

urlpatterns = [
    path('expenses/register/', views.ExpenseRegisterView.as_view(),),  
    path('expenses/list/', views.ExpensesListView.as_view(),),
    path('expenses/list/filter/', views.FilterExpensesListView.as_view(), ),
    path('expenses/update/<id>/', views.ExpenseUpdateView.as_view(),),
    path('expenses/delete/<id>/', views.ExpenseDeleteView.as_view(),),
]