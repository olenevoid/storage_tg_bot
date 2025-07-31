from enum import StrEnum, auto
from telegram import InlineKeyboardButton


NAME_SEPARATOR = '__'
PARAM_SEPARATOR = ','


class Callback(StrEnum):
    TERMS_OF_SERVICE = auto()
    ORDER_STORAGE = auto()
    MY_ORDERS = auto()
    MAIN_MENU = auto()
    COURIER_DELIVERY = auto()    
    SELF_DELIVERY = auto()
    ORDER_DELIVERY = auto()
    PERSONAL_DATA_AGREEMENT = auto()
    DOWNLOAD_PPD = auto()
    HAND_OVER_THINGS = auto()
    SELECT_WAREHOUSE = auto()
    WAREHOUSE = auto()
    MY_BOX = auto()
    INPUT_FULL_NAME = auto()
    INPUT_ADDRESS = auto()
    INPUT_PHONE = auto()
    INPUT_EMAIL = auto()
    BACK_TO_MENU = auto()
    CALL_COURIER = auto()
    SIGN_UP = auto()
    FAQ = auto()
    FORBIDDEN_TO_STORE = auto()
    DOWNLOAD_TOS = auto()
    SHOW_PRICES = auto()
    MY_ACCOUNT = auto()
    CREATE_COURIER_DELIVERY_REQUEST = auto()
    SELECT_BOX = auto()
    SELECT_RENT_PERIOD = auto()
    CONFIRM_BOX_RENT = auto()
    NO_PROMO = auto()
    OPEN_BOX = auto()
    OPEN_QR = auto()
    PUT_NEW_ITEMS = auto()
    REMOVE_ITEMS = auto()
    REMOVE_ITEM = auto()


# Класс для создания строки коллбэков с параметрами 
# и для удобного доступа к имени коллбэка и параметрам
class CallbackData:
    def __init__(self, name: Callback, params: dict = {}):
        self.name: Callback = name
        self.params: dict = params

    @property
    def param_string(self,) -> str:
        if not self.params:
            return ''

        param_string = ''
        for name, value in self.params.items():
            param_string += f'{name}={value}{PARAM_SEPARATOR}'

        return param_string

    def to_str(self) -> str:
        if self.param_string:
            return f'{self.name.value}{NAME_SEPARATOR}{self.param_string}'

        return self.name.value


class CallbackButton(InlineKeyboardButton):
    def __init__(self, text: str, callback_name: Callback, **params):

        callback_data = CallbackData(callback_name, params).to_str()

        super().__init__(
            text,
            callback_data=callback_data,
        )


def get_pattern(callback_name: Callback):
    return f'^({callback_name.value})(?:__.*)?$'


# Парсит строку в класс CallbackData
def parse_callback_data_string(callback_data: str) -> CallbackData:
    parsed_callback = callback_data.split(NAME_SEPARATOR)
    callback_name = Callback(parsed_callback[0])
    callback_params = {}

    if len(parsed_callback) > 1:
        param_pairs = parsed_callback[1].split(PARAM_SEPARATOR)

        for param_pair in param_pairs:
            if param_pair:
                name, value = _parse_param_pair(param_pair)
                callback_params[name] = value

    return CallbackData(callback_name, callback_params)


def _parse_param_pair(param_pair: str) -> tuple:
    name, value = param_pair.split('=')

    if value.isnumeric():
        value = int(value)

    return (name, value)
