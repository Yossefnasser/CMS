from django.http import JsonResponse
from app.models import Patient

def add_patient(request):
    if request.method == 'POST':
        try:
            patient = Patient.objects.create(
                full_name=request.POST.get('full_name'),
                phone_number=request.POST.get('phone'),
                notes=request.POST.get('notes', '')
            )
            
            return JsonResponse({
                'success': True,
                'patient_id': patient.id,
                'patient_name': patient.full_name
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})