from django.urls import path
from goals import views

urlpatterns = [
    path('goals/register/', views.GoalRegisterView.as_view(),),
    path('goals/list/', views.GoalListview.as_view(),),
    path('goals/update/<id>/', views.GoalUpdateView.as_view(),),
    path('goals/delete/<id>/', views.GoalDeleteView.as_view(),)
]