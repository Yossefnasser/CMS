from datetime import datetime
from urllib import request
from django.shortcuts import render
from app.models import Doctor, Specialization
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from app.helpers import check_if_post_input_valid, check_valid_text, get_id_of_object , delete
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from project.settings import CHAR_100, CHAR_50


def list_of_doctors(request):

    return render(request, 'doctors/list.html')

def get_list_of_doctors(request):
    try:
        draw            = int(request.GET.get('draw', 1))
        start           = int(request.GET.get('start', 0))
        length          = int(request.GET.get('length', 10))
        search_value    = request.GET.get('search[value]', '').strip()

        page_number = (start // length) + 1

        # Add ordering to avoid pagination warning
        queryset = Doctor.objects.filter(deleted_date__isnull=True).order_by('id')
        
        if search_value:
            queryset = queryset.filter(
                Q(full_name__icontains=search_value) |
                Q(phone_number__icontains=search_value) |
                Q(id__icontains=search_value)
            )

        paginator = Paginator(queryset, length)
        
        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        # Try-catch around to_json() in case that's where the Fernet error occurs
        data = []
        for doctor in page_obj:
            try:
                data.append(doctor.to_json())
            except Exception as e:
                print(f"Error serializing doctor {doctor.id}: {str(e)}")
                continue

        return JsonResponse({
            "draw": draw,
            "recordsTotal": queryset.count(),
            "recordsFiltered": queryset.count(),
            "data": data
        })

    except Exception as e:
        print(f"Error in get_list_of_doctors: {str(e)}", exc_info=True)
        return JsonResponse({
            "draw": draw if 'draw' in locals() else 0,
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": [],
            "error": str(e)  # Include error message for debugging
        }, status=500)
    

def add_new_doctor(request):
    
    added_by     = request.user
    added_date   = datetime.now()
    updated_date = datetime.now()
    updated_by   = request.user
    typeOfReq    = request.GET.get('type', 'new')

    if typeOfReq == 'edit':
        idOfObject      = get_id_of_object(request.GET.get('id'))
        data_to_insert  = Doctor.objects.get(id=idOfObject)
    elif typeOfReq == 'new':
        data_to_insert = None

    all_specializations = Specialization.objects.filter(deleted_date__isnull=True)
    print(" ------------------------------------    all_specializations   ----------------------------" , all_specializations)

    context = {
        'data_to_insert'        : data_to_insert,
        'typeOfReq'             : typeOfReq,
        'all_specializations'   : all_specializations
    }

    if request.method == 'POST':
        full_name            = check_if_post_input_valid(request.POST['full_name'], CHAR_100)
        email                = request.POST.get('email', '').strip()
        phone_number         = check_if_post_input_valid(request.POST['phone_number'], CHAR_100)
        specialization_id       = request.POST.get('specialization')

        print(" -------------------------- all data --------------------------")
        print("Full Name:", full_name)
        print("Email:", email)
        print("Phone Number:", phone_number)
        print("Specialization ID:", specialization_id)

        specialization_obj = Specialization.objects.filter(id=specialization_id).first()

    

        if typeOfReq == 'edit':
            doctor_obj = Doctor.objects.filter(id=idOfObject).first()

            doctor_obj.full_name               = full_name
            doctor_obj.phone_number            = phone_number
            doctor_obj.email                   = email
            doctor_obj.specialization          = specialization_obj
            doctor_obj.updated_by              = updated_by
            doctor_obj.updated_date            = updated_date
            doctor_obj.save()

        elif typeOfReq == 'new':
            data_to_insert =  Doctor.objects.create(
                full_name           = full_name,
                phone_number        = phone_number,
                email               = email,
                specialization      = specialization_obj , 
                added_by            = added_by,
                added_date          = added_date,
                updated_by          = updated_by,
                updated_date        = updated_date
            )
            print("email is ", data_to_insert.email)
            data_to_insert.save()

        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        return render(request, 'doctors/add.html', context)

def delete_doctor(request):
    doctor_id      = request.POST['id']

    delete(request, Doctor, Q(id = doctor_id))

    allJson             = {"Result": "Fail"}
    allJson['Result']   = "Success"

    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    


def check_if_doctor_exists(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number', '').strip()
        doctor_id   = request.GET.get('id', None)

        if not phone_number:
            return JsonResponse({'exists': False})
        
        query = Doctor.objects.filter(phone_number=phone_number)
        if doctor_id:
            query = query.exclude(id=doctor_id)
            
        doctor = query.first()
        return JsonResponse({
            'exists': doctor is not None,
            'doctor'       : {
                'id'        : doctor.id if doctor else None,
                'name'      : doctor.name if doctor else None,
            }
        })
    return JsonResponse({'exists': False})