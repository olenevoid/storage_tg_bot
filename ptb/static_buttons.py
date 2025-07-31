from ptb.callbacks import Callback, CallbackButton


REMOVE_THINGS = CallbackButton('Забрать вещи', Callback.REMOVE_ITEMS)
ADD_THINGS = CallbackButton('Положить вещи', Callback.PUT_NEW_ITEMS)
OPEN_QR = CallbackButton('Получить QR для открытия', Callback.OPEN_QR)
CONFIRM_RENT = CallbackButton(
    'Подтвердить аренду',
    Callback.CONFIRM_BOX_RENT
)
NO_PROMO = CallbackButton(
    'Нет промокода',
    Callback.NO_PROMO
)
COURIER_DELIVERY_YES = CallbackButton(
    'Подтвердить',
    Callback.CREATE_COURIER_DELIVERY_REQUEST
)
MY_ACCOUNT = CallbackButton(
    'Личный кабинет',
    Callback.MY_ACCOUNT
)
SHOW_PRICES = CallbackButton(
    'Показать расценки',
    Callback.SHOW_PRICES
)
TOS = CallbackButton('Условия хранения/FAQ', Callback.TERMS_OF_SERVICE)

FAQ = CallbackButton(
    'Частые вопросы',
    Callback.FAQ
)
ORDER_STORAGE = CallbackButton(
    'Заказать ячейку',
    Callback.ORDER_STORAGE
)
MY_ORDERS = CallbackButton(
    'Мои заказы',
    Callback.MY_ORDERS
)
TOS_DOWNLOAD = CallbackButton(
    'Скачать условия',
    Callback.DOWNLOAD_TOS
)
BACK_TO_MENU = CallbackButton(
    'В главное меню',
    Callback.MAIN_MENU
)
FORBIDDEN = CallbackButton(
    'Запрещенные к хранению вещества',
    Callback.FORBIDDEN_TO_STORE
)
COURIER_DELIVERY = CallbackButton(
    'Вывоз курьером',
    Callback.COURIER_DELIVERY
)
SELF_DELIVERY = CallbackButton(
    'Привезу сам',
    Callback.SELECT_WAREHOUSE
    )
PPD_YES = CallbackButton(
    'Да',
    Callback.INPUT_FULL_NAME
)
PPD_NO = CallbackButton(
    'Нет',
    Callback.MAIN_MENU
)
PPD_DOWNLOAD = CallbackButton(
    'Скачать полную версию',
    Callback.DOWNLOAD_PPD
)
SIGNUP = CallbackButton(
    'Зарегистрироваться',
    Callback.PERSONAL_DATA_AGREEMENT
)
CONFIRM_SIGNUP = CallbackButton(
    'Подтвердить регистрацию',
    Callback.SIGN_UP
)
CHANGE_PERSONAL_DATA = CallbackButton(
    'Ввести данные заново',
    Callback.PERSONAL_DATA_AGREEMENT
)
