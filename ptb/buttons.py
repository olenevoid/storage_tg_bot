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
    COURIER_DELIVERY = auto()
    SELF_DELIVERY = auto()
    PPD_YES = auto()
    PPD_NO = auto()
    PPD_DOWNLOAD = auto()
    HAND_OVER_THINGS = auto()
    SIGNUP = auto()
    CONFIRM_SIGNUP = auto()
    CHANGE_PERSONAL_DATA = auto()
    SHOW_PRICES = auto()


BUTTONS = {
    ButtonName.SHOW_PRICES: InlineKeyboardButton(
        'Показать расценки',
        callback_data=CallbackData(State.SHOW_PRICES).to_str()
    ),
    ButtonName.TOS: InlineKeyboardButton(
        'Условия хранения/FAQ',
        callback_data=CallbackData(State.TERMS_OF_SERVICE).to_str()
    ),
    ButtonName.FAQ: InlineKeyboardButton(
        'Частые вопросы',
        callback_data=CallbackData(State.FAQ).to_str()
    ),
    ButtonName.ORDER_STORAGE: InlineKeyboardButton(
        'Заказать ячейку',
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
    ButtonName.COURIER_DELIVERY: InlineKeyboardButton(
        'Вывоз курьером',
        callback_data=CallbackData(State.COURIER_DELIVERY).to_str()
    ),
    ButtonName.SELF_DELIVERY: InlineKeyboardButton(
        'Привезу сам',
        callback_data=CallbackData(State.WAREHOUSES).to_str()
        ),
    ButtonName.PPD_YES: InlineKeyboardButton(
        'Да (Продолжить регистрацию)',
        callback_data=CallbackData(State.INPUT_FULL_NAME).to_str()
    ),
    ButtonName.PPD_NO: InlineKeyboardButton(
        'Нет (Вернуться в меню)',
        callback_data=CallbackData(State.MAIN_MENU).to_str()
    ),
    ButtonName.PPD_DOWNLOAD: InlineKeyboardButton(
        'Скачать полную версию',
        callback_data=CallbackData(State.DOWNLOAD_PPD).to_str()
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
