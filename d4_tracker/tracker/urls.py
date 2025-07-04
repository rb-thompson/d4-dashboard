from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('fun_score/', views.fun_score, name='fun_score'),
    # Add other paths as needed
]