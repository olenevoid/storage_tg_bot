from ptb.settings import MAX_RENT_PERIOD
import re


def name_is_valid(full_name: str) -> bool:
    return len(full_name) > 2


def phone_is_valid(phone: str) -> bool:
    pattern = r'^(7|8)\d{10}$'
    return re.match(pattern, phone)


def email_is_valid(email: str) -> bool:
    return len(email) > 2


def period_is_valid(period: str) -> bool:
    return period.isnumeric() and int(period) <= MAX_RENT_PERIOD
