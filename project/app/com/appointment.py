from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from app.helpers import get_id_of_object
from app.models import Appointment, Clinic, Doctor, DoctorSchedule, Patient, Status, User ,Specialization
from django.db.models import Q
import json


from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime

def new_appointment(request):
    added_by     = request.user
    added_date   = datetime.now()
    updated_date = datetime.now()
    updated_by   = request.user
    typeOfReq    = request.GET.get('type', 'new')

    if typeOfReq == 'edit':
        idOfObject      = get_id_of_object(request.GET.get('id'))
        data_to_insert  = Appointment.objects.get(id=idOfObject)
    elif typeOfReq == 'new':
        data_to_insert = None

    # Load needed data for form
    doctors = Doctor.objects.filter(deleted_date__isnull=True)
    clinics = Clinic.objects.filter(deleted_date__isnull=True)
    all_specializations = Specialization.objects.filter(deleted_date__isnull=True)

    context = {
        'doctors'             : doctors,
        'clinics'             : clinics,
        'all_specializations' : all_specializations,
        'data_to_insert'      : data_to_insert,
        'typeOfReq'           : typeOfReq,
    }

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        if not patient_id or not Patient.objects.filter(id=patient_id).exists():
            messages.error(request, 'يرجى اختيار مريض صحيح')
            return redirect('/new-appointment?new')
    

        doctor_id  = request.POST.get('doctor')
        clinic_id  = request.POST.get('clinic')
        status     = request.POST.get('status', 'OPEN')
        status_obj = Status.objects.get(name=status)
        patient_obj = Patient.objects.get(id=patient_id)
        doctor_obj  = Doctor.objects.get(id=doctor_id)
        clinic_obj  = Clinic.objects.get(id=clinic_id)

        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except (ValueError, TypeError):
            messages.error(request, 'صيغة التاريخ أو الوقت غير صحيحة')
            return redirect('/new-appointment?new')

        notes = request.POST.get('notes', '')

        if typeOfReq == 'edit':
            appointment = Appointment.objects.filter(id=idOfObject).first()
            if appointment:
                appointment.patient = patient_obj
                appointment.doctor = doctor_obj
                appointment.clinic = clinic_obj
                appointment.status = status_obj
                appointment.date = date
                appointment.time = time
                appointment.notes = notes
                appointment.updated_by = updated_by
                appointment.updated_date = updated_date
                appointment.save()

        else:  # new
            Appointment.objects.create(
                patient=patient_obj,
                doctor=doctor_obj,
                clinic=clinic_obj,
                status=status_obj,
                date=date,
                time=time,
                notes=notes,
                added_by=added_by,
                added_date=added_date,
                updated_by=updated_by,
                updated_date=updated_date
            )

        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        return render(request, 'appointment/add.html', context)

def new_appointment_api(request):
    cur_user = request.user
    cur_date = timezone.now()
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # ← هنا بنقرأ JSON
            print("Received appointment data:", data)

            # مثال: استخراج البيانات
            doctor_id   = data.get('doctor_id')
            patient_id  = data.get('patient_id')
            date        = data.get('date')
            time_range        = data.get('time')
            day         = data.get('day')
            appt_type   = data.get('type')
            notes       = data.get('notes', '')
            status      = data.get('status', 'OPEN')
            clinic_name = data.get('clinic')
            try : 
                # تقسيم الوقت (start, end)
                start_time, end_time = None, None
                if time_range:
                    parts = time_range.split('-')
                    if len(parts) == 2:
                        start_str = parts[0].strip()  # "10:00"
                        end_str   = parts[1].strip()  # "12:00"
                        start_time = datetime.strptime(start_str, "%H:%M").time()
                        end_time   = datetime.strptime(end_str, "%H:%M").time()
                # status_obj = Status.objects.get(name=status)
                patient_obj = Patient.objects.get(id=patient_id)
                doctor_obj  = Doctor.objects.get(id=doctor_id)
                clinic_obj  = Clinic.objects.filter(name=clinic_name).first() if clinic_name else None

                # clinic_obj  = doctor_schedule.clinic if doctor_schedule.exists() else None
            except Exception as e:
                print("Error occurred while fetching related objects:", e)
                return JsonResponse({"success": False, "message": "خطأ في البيانات"}, status=400)


            try : 

                Appointment.objects.create(
                    patient=patient_obj,
                    doctor=doctor_obj,
                    clinic=clinic_obj,
                    status_id=1,
                    date=date,
                    time=start_time,
                    notes=notes,
                    added_by=cur_user,
                    added_date=cur_date,
                    updated_by=cur_user,
                    updated_date=cur_date
                )
            except Exception as e:
                print("Error occurred while fetching related objects:           222222", e)
                return JsonResponse({"success": False, "message": "خطأ في البيانات"}, status=400)

            return JsonResponse({"success": True, "message": "تم حجز الموعد بنجاح"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"خطأ في البيانات: {str(e)}"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def api_get_doctors_by_specialization(request):
    specialization_id = request.GET.get('specialization')
    print(f"-----------------{specialization_id}-----------------")

    doctors = Doctor.objects.filter(
        specialization__id=specialization_id,
        deleted_date__isnull=True
    )

    return JsonResponse({
        "success": True,
        "doctors": [
            {
                "id": doctor.id,
                "name": doctor.full_name
            }
            for doctor in doctors
        ]
    })

def get_doctor_schedule(request):
    doctor_id = request.GET.get("doctor_id")
    if not doctor_id:
        return JsonResponse({"success": False, "message": "Doctor ID required"}, status=400)

    today       = timezone.now().date()
    schedules   = DoctorSchedule.objects.filter(
        doctor_id=doctor_id,
        is_active=True,
        valid_from__lte=today
    ).filter(
        Q(valid_to__isnull=True) | Q(valid_to__gte=today)
    ).select_related("clinic", "day_of_week")

    data = []
    for sch in schedules:
        data.append({
            "id"            : sch.id,
            "clinic"       : sch.clinic.name,
            "day"          : sch.day_of_week.name,
            "day_id"      : sch.day_of_week.id,
            "start_time"  : sch.start_time.strftime("%H:%M"),
            "end_time"    : sch.end_time.strftime("%H:%M"),
        })
    print(" -------------------------------------   Data: ", data , "--------------------------------------------")

    return JsonResponse({"success": True, "schedules": data})