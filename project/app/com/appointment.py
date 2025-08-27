from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from app.models import Appointment, Clinic, Doctor, Patient, User ,Specialization


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
        all_specializations = Specialization.objects.all()
        context = {
            'doctors': doctors,
            'clinics': clinics,
            'all_specializations': all_specializations,
        }
        return render(request, 'appointment/add.html', context)
def api_get_doctors_by_specialization(request):
    specialization__id = request.GET.get('specialization')
    print(f"-----------------{specialization__id}-----------------")
    doctors = Doctor.objects.filter(
        specialization__id=specialization__id,
        deleted_date__isnull=True
    )
    return JsonResponse({
        "success" : True,
        "doctors" : [doctors.to_json()for doctors in doctors]
    })
def api_search_patients(request):
    identifier = request.GET.get('identifier').strip()
    print(f"-----------{identifier}----------")
    patient = Patient.objects.filter(
        phone_number=identifier,
        deleted_date__isnull=True
    ).first()
    print("Patient found:", patient)
    return JsonResponse({
        "success" : True,
        "found" : True,
        'patient' : patient.to_json() if p0atient else None
    })