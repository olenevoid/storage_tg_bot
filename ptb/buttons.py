from telegram import InlineKeyboardButton
from ptb.callbacks import CallbackData, State
from enum import Enum, auto


class ButtonName(Enum):
    TOS = auto()
    FAQ = auto()
    ORDER_STORAGE = auto()
    MY_ORDERS = auto()
    TOS_DOWNLOAD = auto()
    BACK_TO_MENU = auto()
    FORBIDDEN = auto()
    FREE_REMOVAL = auto()
    SELF_DELIVERY = auto()
    PPD_YES = auto()
    PPD_NO = auto()
    HAND_OVER_THINGS = auto()
    SIGNUP = auto()
    CONFIRM_SIGNUP = auto()
    CHANGE_PERSONAL_DATA = auto()


BUTTONS = {
    ButtonName.TOS: InlineKeyboardButton(
        'Условия хранения/FAQ',
        callback_data=CallbackData(State.TERMS_OF_SERVICE).to_str()
    ),
    ButtonName.FAQ: InlineKeyboardButton(
        'Частые вопросы',
        callback_data=CallbackData(State.FAQ).to_str()
    ),
    ButtonName.ORDER_STORAGE: InlineKeyboardButton(
        'Выбрать склад',
        callback_data=CallbackData(State.ORDER_STORAGE).to_str()
    ),
    ButtonName.MY_ORDERS: InlineKeyboardButton(
        'Мои заказы',
        callback_data=CallbackData(State.MY_ORDERS).to_str()
    ),
    ButtonName.TOS_DOWNLOAD: InlineKeyboardButton(
        'Скачать условия',
        callback_data=CallbackData(State.DOWNLOAD_TOS).to_str()
    ),
    ButtonName.BACK_TO_MENU: InlineKeyboardButton(
        'В главное меню',
        callback_data=CallbackData(State.MAIN_MENU).to_str()
    ),
    ButtonName.FORBIDDEN: InlineKeyboardButton(
        'Запрещенные к хранению вещества',
        callback_data=CallbackData(State.FORBIDDEN_TO_STORE).to_str()
    ),
    ButtonName.FREE_REMOVAL: InlineKeyboardButton('Бесплатный вывоз', callback_data='free_removal'),
    ButtonName.SELF_DELIVERY: InlineKeyboardButton('Доставлю сам', callback_data='self_delivery'),
    ButtonName.PPD_YES: InlineKeyboardButton(
        'Да',
        callback_data=CallbackData(State.INPUT_FULL_NAME).to_str()
    ),
    ButtonName.PPD_NO: InlineKeyboardButton(
        'Нет (назад в меню)',
        callback_data=CallbackData(State.MAIN_MENU).to_str()
        ),
    ButtonName.HAND_OVER_THINGS: InlineKeyboardButton('Сдать вещи', callback_data='hand_over_things'),
    ButtonName.SIGNUP: InlineKeyboardButton(
        'Зарегистрироваться',
        callback_data=CallbackData(State.PERSONAL_DATA_AGREEMENT).to_str()
    ),
    ButtonName.CONFIRM_SIGNUP: InlineKeyboardButton(
        'Подтвердить регистрацию',
        callback_data=CallbackData(State.SIGN_UP).to_str()
    ),
    ButtonName.CHANGE_PERSONAL_DATA: InlineKeyboardButton(
        'Ввести данные заново',
        callback_data=CallbackData(State.PERSONAL_DATA_AGREEMENT).to_str()
    )
}