from enum import Enum, auto


NAME_SEPARATOR = '__'
PARAM_SEPARATOR = ','


# Enum для управления коллбэками. 
# Можно быстро переименовать в одном месте, если понадобится
class CallbackName(Enum):
    FAQ = 'faq'
    ORDER_STORAGE = 'order_storage'
    MY_ORDERS = 'my_orders'
    MAIN_MENU = 'main_menu'
    BACK = 'back'
    FREE_REMOVAL = 'free_removal'
    SELF_DELIVERY = 'self_delivery'
    ORDER_DELIVERY = 'order_delivery'
    PERSONAL_DATA_AGREE = 'pd_yes'
    PERSONAL_DATA_DISAGREE = 'pd_no'
    HAND_OVER_THINGS = 'hand_over_things'
    OK = 'ok'
    WAREHOUSE = 'warehouse'
    MY_BOX = 'my_box'


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
