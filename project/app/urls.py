from django.urls import path, include

from .com import auth, dashboard ,patient ,appointment,doctors

urlpatterns = [
    path('',            dashboard.dashboard, name='dashboard'),

    path('auth/login',  auth.login_view, name='login'),
    path('auth/logout', auth.logout_view, name='logout'),
    
    path('doctors', doctors.doctors, name='doctors'),
    path('doctors/add', doctors.add_new_doctor, name='add-new-doctor'),
    
    path('add-patient',      patient.add_new_patient, name='add-patient'),
    path('list-of-patients', patient.list_of_patient, name='list-of-patients'),
    path('check-patient/',   patient.chech_if_patient_exists, name='chech-if-patient-exists'),


    path('add-appointment', appointment.new_appointment, name='add-appointment'),


]
