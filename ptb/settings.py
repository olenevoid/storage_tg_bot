from environs import env
from enum import Enum, auto


env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
BUTTONS_PER_PAGE = 4


class State(Enum):
    MAIN_MENU = auto()
    MY_ACCOUNT = auto()
    TERMS_OF_SERVICE = auto()
    ORDER_STORAGE = auto()
    SELECT_WAREHOUSE = auto()
    WAREHOUSE = auto()
    INPUT_ADDRESS = auto()
    MY_ORDERS = auto()
    MY_BOX = auto()
    PERSONAL_DATA_AGREEMENT = auto()
    INPUT_FULL_NAME = auto()
    INPUT_PHONE = auto()
    INPUT_EMAIL = auto()
    SIGN_UP = auto()
    FINAL = auto()


# Значения должны совпадать с ролями в БД
class RoleName(Enum):
    Administrator = 'Администратор'
    Courier = 'Курьер'
    Client = 'Клиент'