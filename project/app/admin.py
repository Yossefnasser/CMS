from django.contrib import admin
from .models import Doctor, User, Patient, Clinic, DoctorSchedule, Appointment, Invoice ,Status,Specialization,DaysOfWeek

admin.site.register(User)
admin.site.register(Specialization)
admin.site.register(Status)
admin.site.register(Patient)
admin.site.register(Clinic)
admin.site.register(Doctor)
admin.site.register(DoctorSchedule)
admin.site.register(Appointment)
admin.site.register(Invoice)
admin.site.register(DaysOfWeek)