from datetime import datetime
from django.shortcuts import render

from app.models import Doctor



def doctors(request):
    doctors_list = Doctor.objects.all()
    context = {
        'doctors': doctors_list,
    }
    
    if request.method == 'POST':
        # Handle any POST requests if needed
        pass

    # Render the doctors template with the context
    return render(request, 'doctors/doctors.html',context)

def add_new_doctor(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        specialization = request.POST.get('specialization')
        added_by     = request.user
        added_date   = datetime.now()
        updated_date = datetime.now()
        updated_by   = request.user
        new_doctor = Doctor.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            specialization=specialization,
            added_by=added_by,
            added_date=added_date,
            updated_by=updated_by,
            updated_date=updated_date
        )
        new_doctor.save()
        doctors_list = Doctor.objects.all()
        context = {
            'doctors': doctors_list,
            'success': 'Doctor added successfully.'
        }
        return render(request, 'doctors/doctors.html', context)
    elif request.method == 'GET':
      return render(request, 'doctors/add.html')