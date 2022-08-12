from django.urls import path
from balance import views

urlpatterns = [ 
    path('balance/list/filter/',views.Get.as_view(),),
]