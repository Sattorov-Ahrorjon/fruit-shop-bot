import re


def regex_phone(phone: str):
    return re.match(pattern=r'^\+998\d{9}$', string=phone)
