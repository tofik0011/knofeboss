import errno
import os
import re

import requests
from django.core.files import File

from unine_engine.globals import MEDIA_ROOT


def print_c(text):
    with open(f"{MEDIA_ROOT}/files/log.txt", 'w+') as f:
        myfile = File(f)
        myfile.write(str(text))


def download(url, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    try:
        with open(file_name, "wb") as file:
            response = requests.get(url, timeout=0.5, allow_redirects=True)
            print(response.status_code, url)
            file.write(response.content)
    except Exception as ex:
        print(ex)


def validate_phone(phone):
    """Валидация номера телефона"""
    if re.match("^(?:[0-9]●?){6,14}[0-9]$", phone) is not None:
        return True
    else:
        return False


def validate_email(email):
    """Валидация ел. почты"""
    if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) is not None:
        return True
    else:
        return False


def trim_phone(phone):
    return re.sub(r"\D+", '', phone)
