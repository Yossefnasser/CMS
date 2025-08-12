from django.urls import path, include
from .com import dashboard

urlpatterns = [
    path('', dashboard.dashboard, name='dashboard'),
]
