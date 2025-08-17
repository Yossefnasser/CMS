from datetime import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from app.helpers import check_if_post_input_valid, check_valid_text, get_id_of_object
from app.models import Patient
from project.settings import CHAR_100
####################  Patient  #################3


def list_of_patient(request):

    return render(request,'patient/list.html',None)




def add_new_patient(request):
    added_by     = request.user
    added_date   = datetime.now()
    updated_date = datetime.now()
    updated_by   = request.user
    typeOfReq    = request.GET.get('type', 'new')

    if typeOfReq == 'edit':
        idOfObject      = get_id_of_object(request.GET.get('id'))
        data_to_insert  = Patient.objects.get(id=idOfObject)
    elif typeOfReq == 'new':
        data_to_insert = None

    context = {
        'data_to_insert': data_to_insert,
        'typeOfReq': typeOfReq,
    }

    if request.method == 'POST':
        full_name            = check_if_post_input_valid(request.POST['full_name'], CHAR_100)
        phone_number         = check_if_post_input_valid(request.POST['phone'], CHAR_100)
        notes                = check_valid_text(request.POST['notes'])
        age                  = check_if_post_input_valid(request.POST['age'], CHAR_100)
        gender               = request.POST['gender']

        print(" ------------------------------------    data   ----------------------------" , full_name , phone_number ,  notes ,  age  , gender)


        if typeOfReq == 'edit':
            patient_obj = Patient.objects.filter(id=idOfObject).first()

            patient_obj.full_name    = full_name
            patient_obj.phone_number = phone_number
            patient_obj.notes        = notes
            patient_obj.updated_by   = updated_by
            patient_obj.updated_date = updated_date
            patient_obj.save()

        elif typeOfReq == 'new':
            patient_obj = Patient.objects.filter(phone_number=phone_number).first()
            data_to_insert =  Patient.objects.create(
                full_name    = full_name,
                phone_number = phone_number,
                notes        = notes,
                age          = age , 
                gender       = gender ,
                added_by     = added_by,
                added_date   = added_date,
                updated_by   = updated_by,
                updated_date = updated_date
            )
            data_to_insert.save()

        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        return render(request, 'patient/add.html', context)


def chech_if_patient_exists(request):
    phone_number = request.GET.get('phone_number', None)
    if not phone_number:
        return JsonResponse({'exists': False})

    patient = Patient.objects.filter(phone_number=phone_number).first()
    if patient:
        return JsonResponse({'exists': True, 'id': patient.id})
    else:
        return JsonResponse({'exists': False})