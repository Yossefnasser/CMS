
from django.http import JsonResponse
from project.settings import key_hashing
from cryptography.fernet import Fernet
import uuid
import datetime as dt
import re
from project.settings import CHAR_05, CHAR_10, CHAR_15
from django import template

register = template.Library()

@register.simple_tag
def get_id_hashed_of_object(object_id):
    fernet = Fernet(key_hashing)
    encMessage = fernet.encrypt(str(object_id).encode())
    out = (encMessage).decode('ascii')
    return str(out)

def check_if_post_input_valid(text, max_length): 
    if not isinstance(text, str) or text.strip() == '':
        return ''

    pattern = r"^[\S\s][a-zA-Z0-9\u0600-\u06FF\s\)\(\\\/\_\-\³\%]{1," + str(max_length) + r"}\s*$"
    check = re.search(pattern, text)

    if check is not None:
        text = text.strip()
        return text[:max_length] if len(text) > max_length else text
    else:
        return ''
    


def check_valid_text(text):
    check = re.search(r"^/var\s*.*;/g*$", text)
    if check is None:
        return text
    else:
        return ''
    
def get_id_of_object(hash_used):
    decMessage = None
    try :
        fernet = Fernet(key_hashing)
        decMessage = fernet.decrypt(str(hash_used)).decode()
    except Exception as err:
        pass

    return decMessage


def delete(request, model_name, condition):
    deleted_date            = dt.datetime.now()
    object                  = model_name.objects.filter(condition)
    _id                     = '_' + str(object[0].id)  + '_DELETED'

    object.update(deleted_by=request.user, deleted_date = deleted_date)

    allJson = {"Result": "Fail"}

    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
