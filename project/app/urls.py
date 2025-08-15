from django.urls import path, include

from .com import auth, dashboard ,patient

urlpatterns = [
    path('',            dashboard.dashboard, name='dashboard'),

    path('auth/login',  auth.login_view, name='login'),
    path('auth/logout', auth.logout_view, name='logout'),

    path('add-patient',      patient.add_new_patient, name='add-patient'),
    path('list-of-patients', patient.list_of_patient, name='list-of-patients'),
]
