from enum import Enum, auto
from telegram import InlineKeyboardButton


NAME_SEPARATOR = '__'
PARAM_SEPARATOR = ','


# Enum для управления коллбэками
# Можно быстро переименовать в одном месте, если понадобится
# Текст коллбэка должен быть уникальным
class CallbackName(Enum):
    TERMS_OF_SERVICE = 'tos'
    ORDER_STORAGE = 'order_storage'
    MY_ORDERS = 'my_orders'
    MAIN_MENU = 'main_menu'
    COURIER_DELIVERY = 'free_removal'    
    SELF_DELIVERY = 'self_delivery'
    ORDER_DELIVERY = 'order_delivery'
    PERSONAL_DATA_AGREEMENT = 'ppd'
    DOWNLOAD_PPD = 'download_ppd'
    HAND_OVER_THINGS = 'hand_over_things'
    SELECT_WAREHOUSE = 'select_warehouse'
    WAREHOUSE = 'warehouse_details'
    MY_BOX = 'my_box'
    INPUT_FULL_NAME = 'input_full_name'
    INPUT_ADDRESS = 'input_address'
    INPUT_PHONE = 'input_phone'
    INPUT_EMAIL = 'input_email'
    FINAL = 'final'
    BACK_TO_MENU = 'unknown'
    CALL_COURIER = 'call_courier'
    SIGN_UP = 'sign_up'
    FAQ = 'faq'
    FORBIDDEN_TO_STORE = 'forbidden'
    DOWNLOAD_TOS = 'tos_download'
    SHOW_PRICES = 'show_prices'
    MY_ACCOUNT = 'my_account'
    CREATE_COURIER_DELIVERY_REQUEST = 'create_delivery_request'
    SELECT_BOX = 'select_box'
    SELECT_RENT_PERIOD = 'select_period'
    CONFIRM_BOX_RENT = 'confirm_box_rent'
    NO_PROMO = 'no_promo'
    OPEN_BOX = 'open_box'
    OPEN_QR = 'open_qr'
    PUT_NEW_ITEMS = 'add_things'
    REMOVE_ITEMS = 'remove_things'
    REMOVE_ITEM = 'remove_item'
    # Эти, возможно, не нужны
    BACK = 'back'
    PERSONAL_DATA_AGREE = 'pd_yes'
    PERSONAL_DATA_DISAGREE = 'pd_no'
    OK = 'ok'


# Класс для создания строки коллбэков с параметрами 
# и для удобного доступа к имени коллбэка и параметрам
class CallbackData:
    def __init__(self, name: CallbackName, params: dict = {}):
        self.name: CallbackName = name
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
    def __init__(
        self,
        text: str,
        callback_name: CallbackName,
        **params
    ):

        url = None
        switch_inline_query = None
        switch_inline_query_current_chat = None
        callback_game = None
        pay = None
        login_url = None
        web_app = None
        switch_inline_query_chosen_chat = None
        copy_text = None
        api_kwargs = None

        callback_data = CallbackData(callback_name, params).to_str()

        super().__init__(
            text,
            url,
            callback_data,
            switch_inline_query,
            switch_inline_query_current_chat,
            callback_game,
            pay,
            login_url,
            web_app,
            switch_inline_query_chosen_chat,
            copy_text,
            api_kwargs=api_kwargs)


def get_pattern(callback_name: CallbackName):
    return f'^({callback_name.value})(?:__.*)?$'


# Парсит строку в класс CallbackData
def parse_callback_data_string(callback_data: str) -> CallbackData:
    parsed_callback = callback_data.split(NAME_SEPARATOR)
    callback_name = CallbackName(parsed_callback[0])
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
