from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.my_model_list, name='my_model_list'),
]
