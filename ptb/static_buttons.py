from ptb.callbacks import CallbackName, CallbackButton


REMOVE_THINGS = CallbackButton('Забрать вещи', CallbackName.REMOVE_ITEMS)
ADD_THINGS = CallbackButton('Положить вещи', CallbackName.PUT_NEW_ITEMS)
OPEN_QR = CallbackButton('Получить QR для открытия', CallbackName.OPEN_QR)
CONFIRM_RENT = CallbackButton(
    'Подтвердить аренду',
    CallbackName.CONFIRM_BOX_RENT
)
NO_PROMO = CallbackButton(
    'Нет промокода',
    CallbackName.NO_PROMO
)
COURIER_DELIVERY_YES = CallbackButton(
    'Подтвердить',
    CallbackName.CREATE_COURIER_DELIVERY_REQUEST
)
MY_ACCOUNT = CallbackButton(
    'Личный кабинет',
    CallbackName.MY_ACCOUNT
)
SHOW_PRICES = CallbackButton(
    'Показать расценки',
    CallbackName.SHOW_PRICES
)
TOS = CallbackButton('Условия хранения/FAQ', CallbackName.TERMS_OF_SERVICE)

FAQ = CallbackButton(
    'Частые вопросы',
    CallbackName.FAQ
)
ORDER_STORAGE = CallbackButton(
    'Заказать ячейку',
    CallbackName.ORDER_STORAGE
)
MY_ORDERS = CallbackButton(
    'Мои заказы',
    CallbackName.MY_ORDERS
)
TOS_DOWNLOAD = CallbackButton(
    'Скачать условия',
    CallbackName.DOWNLOAD_TOS
)
BACK_TO_MENU = CallbackButton(
    'В главное меню',
    CallbackName.MAIN_MENU
)
FORBIDDEN = CallbackButton(
    'Запрещенные к хранению вещества',
    CallbackName.FORBIDDEN_TO_STORE
)
COURIER_DELIVERY = CallbackButton(
    'Вывоз курьером',
    CallbackName.COURIER_DELIVERY
)
SELF_DELIVERY = CallbackButton(
    'Привезу сам',
    CallbackName.SELECT_WAREHOUSE
    )
PPD_YES = CallbackButton(
    'Да',
    CallbackName.INPUT_FULL_NAME
)
PPD_NO = CallbackButton(
    'Нет',
    CallbackName.MAIN_MENU
)
PPD_DOWNLOAD = CallbackButton(
    'Скачать полную версию',
    CallbackName.DOWNLOAD_PPD
)
SIGNUP = CallbackButton(
    'Зарегистрироваться',
    CallbackName.PERSONAL_DATA_AGREEMENT
)
CONFIRM_SIGNUP = CallbackButton(
    'Подтвердить регистрацию',
    CallbackName.SIGN_UP
)
CHANGE_PERSONAL_DATA = CallbackButton(
    'Ввести данные заново',
    CallbackName.PERSONAL_DATA_AGREEMENT
)
