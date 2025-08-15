
from project.settings import key_hashing
from cryptography.fernet import Fernet
import uuid
import re
from project.settings import CHAR_05, CHAR_10, CHAR_15


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
    check = re.search("^/var\s*.*;/g*$", text)
    print(check)
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

