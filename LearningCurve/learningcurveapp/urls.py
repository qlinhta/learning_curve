from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.add, name='login'),
]