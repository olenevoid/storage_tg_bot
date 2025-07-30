from telegram import InlineKeyboardButton
from ptb.callbacks import CallbackData, CallbackName


REMOVE_THINGS = InlineKeyboardButton(
    'Забрать вещи',
    callback_data=CallbackData(CallbackName.REMOVE_ITEMS).to_str()
)
ADD_THINGS = InlineKeyboardButton(
    'Положить вещи',
    callback_data=CallbackData(CallbackName.PUT_NEW_ITEMS).to_str()
)
OPEN_QR = InlineKeyboardButton(
    'Получить QR для открытия',
    callback_data=CallbackData(CallbackName.OPEN_QR).to_str()
)
CONFIRM_RENT = InlineKeyboardButton(
    'Подтвердить аренду',
    callback_data=CallbackData(CallbackName.CONFIRM_BOX_RENT).to_str()
)
NO_PROMO = InlineKeyboardButton(
    'Нет промокода',
    callback_data=CallbackData(CallbackName.NO_PROMO).to_str()
)
COURIER_DELIVERY_YES = InlineKeyboardButton(
    'Подтвердить',
    callback_data=CallbackData(
        CallbackName.CREATE_COURIER_DELIVERY_REQUEST
        ).to_str()
)
MY_ACCOUNT = InlineKeyboardButton(
    'Личный кабинет',
    callback_data=CallbackData(CallbackName.MY_ACCOUNT).to_str()
)
SHOW_PRICES = InlineKeyboardButton(
    'Показать расценки',
    callback_data=CallbackData(CallbackName.SHOW_PRICES).to_str()
)
TOS = InlineKeyboardButton(
    'Условия хранения/FAQ',
    callback_data=CallbackData(CallbackName.TERMS_OF_SERVICE).to_str()
)
FAQ = InlineKeyboardButton(
    'Частые вопросы',
    callback_data=CallbackData(CallbackName.FAQ).to_str()
)
ORDER_STORAGE = InlineKeyboardButton(
    'Заказать ячейку',
    callback_data=CallbackData(CallbackName.ORDER_STORAGE).to_str()
)
MY_ORDERS = InlineKeyboardButton(
    'Мои заказы',
    callback_data=CallbackData(CallbackName.MY_ORDERS).to_str()
)
TOS_DOWNLOAD = InlineKeyboardButton(
    'Скачать условия',
    callback_data=CallbackData(CallbackName.DOWNLOAD_TOS).to_str()
)
BACK_TO_MENU = InlineKeyboardButton(
    'В главное меню',
    callback_data=CallbackData(CallbackName.MAIN_MENU).to_str()
)
FORBIDDEN = InlineKeyboardButton(
    'Запрещенные к хранению вещества',
    callback_data=CallbackData(CallbackName.FORBIDDEN_TO_STORE).to_str()
)
COURIER_DELIVERY = InlineKeyboardButton(
    'Вывоз курьером',
    callback_data=CallbackData(CallbackName.COURIER_DELIVERY).to_str()
)
SELF_DELIVERY = InlineKeyboardButton(
    'Привезу сам',
    callback_data=CallbackData(CallbackName.SELECT_WAREHOUSE).to_str()
    )
PPD_YES = InlineKeyboardButton(
    'Да',
    callback_data=CallbackData(CallbackName.INPUT_FULL_NAME).to_str()
)
PPD_NO = InlineKeyboardButton(
    'Нет',
    callback_data=CallbackData(CallbackName.MAIN_MENU).to_str()
)
PPD_DOWNLOAD = InlineKeyboardButton(
    'Скачать полную версию',
    callback_data=CallbackData(CallbackName.DOWNLOAD_PPD).to_str()
)
HAND_OVER_THINGS = InlineKeyboardButton('Сдать вещи', callback_data='hand_over_things')
SIGNUP = InlineKeyboardButton(
    'Зарегистрироваться',
    callback_data=CallbackData(CallbackName.PERSONAL_DATA_AGREEMENT).to_str()
)
CONFIRM_SIGNUP = InlineKeyboardButton(
    'Подтвердить регистрацию',
    callback_data=CallbackData(CallbackName.SIGN_UP).to_str()
)
CHANGE_PERSONAL_DATA = InlineKeyboardButton(
    'Ввести данные заново',
    callback_data=CallbackData(CallbackName.PERSONAL_DATA_AGREEMENT).to_str()
)

