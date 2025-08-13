from django.http import HttpResponse
from django.shortcuts import render
from project.app.models import Clinic, Patient, User


def new_appointment(request):
    patient_id = request.GET.get('patient_id')
    
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
            # Return just the appointment form HTML
            return render(request, 'appointment_form.html', {
                'patient': patient,
                'doctors': User.objects.filter(user_type='DOCTOR'),
                'clinics': Clinic.objects.all()
            })
        except Patient.DoesNotExist:
            pass
    
    return HttpResponse('Patient not found', status=404)