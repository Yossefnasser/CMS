from django.contrib import admin
from .models import User, Patient, Clinic, DoctorSchedule, Appointment, Invoice

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Clinic)
admin.site.register(DoctorSchedule)
admin.site.register(Appointment)
admin.site.register(Invoice)