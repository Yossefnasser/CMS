from django.urls import path, include

from .com import auth, dashboard ,patient ,appointment,doctors

urlpatterns = [
    path('',            dashboard.dashboard, name='dashboard'),

    path('auth/login',  auth.login_view, name='login'),
    path('auth/logout', auth.logout_view, name='logout'),

    path('list-of-doctors', doctors.list_of_doctors, name='list-of-doctors'),
    path('get-list-of-doctors', doctors.get_list_of_doctors, name='get-list-of-doctors'),
    path('add-doctor',  doctors.add_new_doctor, name='add-doctor'),
    path('delete-doctor',   doctors.delete_doctor, name='delete-doctor'),
    path('check-if-doctor-exists', doctors.check_if_doctor_exists, name='check-if-doctor-exists'),
    
    path('doctor-schedule/add/', doctors.doctor_schedule, name='add-doctor-schedule'),
    path('doctor-schedule/update/<int:schedule_id>/', doctors.doctor_schedule, name='update-doctor-schedule'),
    path('doctor-schedule/delete/<int:schedule_id>/',doctors.delete_doctor_schedule, name='delete-doctor-schedule'),
    path('api/time-slots/',doctors.api_get_slots, name='api-get-slots'),
    
    path('add-patient',              patient.add_new_patient,           name='add-patient'),
    path('list-of-patients',         patient.list_of_patient,           name='list-of-patients'),
    path('get-list-of-patients',     patient.get_list_of_patients,      name='get-list-of-patients'),
    path('delete-patient',           patient.delete_patient,            name='delete-patient'),
    path('check-if-patient-exists',  patient.check_if_patient_exists,   name='check-if-patient-exists'),
    
    path('add-appointment', appointment.new_appointment, name='add-appointment'),
    path('list-of-oppointments',appointment.list_of_appointments , name= 'list-of-appointments'),
    path('api/new-appointment', appointment.new_appointment_api, name='api_new_appointment'),
    path('schedules-overview/', appointment.schedules_overview, name='api_schedules-overview-refresh'),
    path('api/get-doctors-by-specialization', appointment.api_get_doctors_by_specialization, name='api_get_doctors_by_specialization'),
    path('api/get-doctor-schedule', appointment.get_doctor_schedule, name='get_doctor_schedule'),
]
