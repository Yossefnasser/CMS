from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Appointment, Clinic, Doctor, Patient, User


def new_appointment(request):
    if request.method == 'POST':
        pateint = Patient.objects
        doctor_id = request.POST.get('doctor')
        clinic_id = request.POST.get('clinic')
        date = request.POST.get('date')
        time = request.POST.get('time')
        created_at = datetime.now()
        updated_at = datetime.now()
        notes = request.POST.get('notes', '')
        status = request.POST.get('status', 'OPEN')
        
        datato_insert = Appointment(
            patient=Patient.objects.get(id=pateint),
            doctor=User.objects.get(id=doctor_id),
            clinic=Clinic.objects.get(id=clinic_id),
            date=date,
            time=time,
            notes=notes,
            status=status,
            created_at=created_at,
            updated_at=updated_at
        )
        datato_insert.save()
        return HttpResponse("Appointment created successfully.")
    elif request.method == 'GET':
        
        doctors = Doctor.objects.all()
        clinics = Clinic.objects.all()
        context = {
            'doctors': doctors,
            'clinics': clinics,
        }
        return render(request, 'appointment/new.html', context)
        