import string
import random
import base64
import uuid
from pydash import _


EMAIL_GENERATED = []


def uuid_base32():
    return base64.b32encode(uuid.uuid4().bytes).decode("utf-8").rstrip('=\n')


def uuid_email():
    temp = uuid_base32()
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    while True:
        email = temp[:18] + "@" + temp[18:] + "." + suffix
        if email not in EMAIL_GENERATED:
            EMAIL_GENERATED.append(email)
            break
    return email


def create_file(file_path, content=None):
    with open(file_path, "w") as fp:
        fp.write(content or "Your text goes here")


def sorting_order(single_column_data, sort_value):

    flag = 0
    if sort_value == "ascending":
        if all(single_column_data[i] <= single_column_data[i + 1] for i in range(len(single_column_data) - 1)):
            flag = 1
    elif sort_value == "descending":
        if all(single_column_data[i] >= single_column_data[i + 1] for i in range(len(single_column_data) - 1)):
            flag = 1
    return flag
