from django.urls import path, include

from .com import auth, dashboard ,new_patient

urlpatterns = [
    path('', dashboard.dashboard, name='dashboard'),
    path('auth/login', auth.login_view, name='login'),
    path('auth/logout', auth.logout_view, name='logout'),
    path('add-patient/', new_patient.add_patient, name='add_patient'),
]
