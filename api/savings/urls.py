from django.urls import path
from savings import views

urlpatterns = [
    path('savings/register/', views.SavingRegisterView.as_view(),),
    path('savings/list/', views.SavingListView.as_view(),),
    path('savings/list/filter/', views.FilterSavingListView.as_view(),),
    path('savings/update/<int:id>/', views.SavingUpdateView.as_view(),),
    path('savings/delete/<int:id>/', views.SavingDeleteView.as_view(),),
]