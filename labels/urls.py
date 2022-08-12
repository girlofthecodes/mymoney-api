from django.urls import path
from labels import views

urlpatterns = [
    path('labels/register/', views.LabelRegisterView.as_view(), ),
    path('labels/list/', views.LabelsListView.as_view(), ),
    path('labels/list/filter/', views.FilterLabelsListView.as_view(), ),
    path('labels/update/<int:id>/', views.LabelUpdateView.as_view(), ),
    path('labels/delete/<int:id>/', views.LabelDeleteView.as_view(), ),
]