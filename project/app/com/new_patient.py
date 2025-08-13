from django.http import JsonResponse
from app.models import Patient

def add_patient(request):
    if request.method == 'POST':
        full_name      =   request.POST.get('full_name')
        phone_number   =   request.POST.get('phone')
        notes          =   request.POST.get('notes', '')

        patient_obj    = Patient.objects.filter(phone_number=phone_number).first()
        if patient_obj:
            return JsonResponse({
                'success': False,
                'error': 'المريض مسجل بالفعل',
                
            })

        try:
            patient = Patient.objects.create(
                full_name      =   full_name,
                phone_number   =   phone_number,
                notes          =   notes
            )
            
            return JsonResponse({
                'success': True,
                'patient_id': patient.id,
                'patient_name': patient.full_name,
                'message': 'تم إضافة المريض بنجاح'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})