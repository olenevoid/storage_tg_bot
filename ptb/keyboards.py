from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, CallbackName
from django.core.paginator import Page
from ptb.buttons import BUTTONS, ButtonName
from ptb.settings import State
from enum import Enum, auto


def main_keyboard(client: dict = None):

    buttons = [
        [BUTTONS[ButtonName.TOS]],
        [BUTTONS[ButtonName.ORDER_STORAGE]],
    ]

    if client:
        buttons.append([BUTTONS[ButtonName.MY_ACCOUNT]])
    else:
        buttons.append([BUTTONS[ButtonName.SIGNUP]])

    return InlineKeyboardMarkup(buttons)


def tos_keyboard():
    return InlineKeyboardMarkup(
        [
            [BUTTONS[ButtonName.TOS_DOWNLOAD]],
            [BUTTONS[ButtonName.FAQ]],
            [BUTTONS[ButtonName.FORBIDDEN]],
            [BUTTONS[ButtonName.BACK_TO_MENU]],
        ]
    )


def back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [BUTTONS[ButtonName.BACK_TO_MENU]],
        ]
    )


def order_storage_keyboard():
    return InlineKeyboardMarkup(
        [
            [BUTTONS[ButtonName.SHOW_PRICES]],
            [BUTTONS[ButtonName.COURIER_DELIVERY]],
            [BUTTONS[ButtonName.SELF_DELIVERY]],
            [BUTTONS[ButtonName.BACK_TO_MENU]],
        ]
    )


def ppd_peyboard():
    return InlineKeyboardMarkup(
        [
            [BUTTONS[ButtonName.PPD_DOWNLOAD]],
            [
                BUTTONS[ButtonName.PPD_YES],
                BUTTONS[ButtonName.PPD_NO]
            ],
        ]
    )


def call_courirer_keyboard():
    return InlineKeyboardMarkup(
        [
            [BUTTONS[ButtonName.HAND_OVER_THINGS]],
            [BUTTONS[ButtonName.BACK_TO_MENU]],
        ]
    )


def _get_page_buttons(page: Page, callback_name: CallbackName):
    page_buttons = []

    if page.has_previous():
        callback_data = CallbackData(
            callback_name,
            params={'page': page.previous_page_number()}
        )
        page_buttons.append(
            InlineKeyboardButton('<--', callback_data=callback_data.to_str())
        )

    if page.has_next():
        callback_data = CallbackData(
            callback_name,
            params={'page': page.next_page_number()}
        )
        page_buttons.append(
            InlineKeyboardButton('-->', callback_data=callback_data.to_str())
        )

    return page_buttons


def warehouses_keyboard(page: Page):
    buttons = []

    warehouses = page.object_list

    for warehouse in warehouses:

        callback_data = CallbackData(
            CallbackName.WAREHOUSE,
            {'id': warehouse.get('id')}
        )

        button = [
            InlineKeyboardButton(
                warehouse.get('name'),
                callback_data=callback_data.to_str()
            ),
        ]
        buttons.append(button)

    buttons.append(_get_page_buttons(page, CallbackName.SELECT_WAREHOUSE))

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def my_orders_keyboard(page: Page):
    buttons = []

    boxes = page.object_list

    for box in boxes:
        callback_data = CallbackData(
            CallbackName.MY_BOX,
            {'id': box.get('id')}
        )

        text = f'Размер {box.get('size')} на {box.get('location')}'

        button = [
            InlineKeyboardButton(
                text,
                callback_data=callback_data.to_str()
            )
        ]

        buttons.append(button)

    buttons.append(_get_page_buttons(page, CallbackName.MY_ORDERS))

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def my_box_keyboard(box_id):

    self_delivery_callback = CallbackData(
        CallbackName.SELECT_WAREHOUSE,
        {'box_id': box_id}
    )

    order_delivery_callback = CallbackData(
        CallbackName.ORDER_DELIVERY,
        {'box_id': box_id}
    )

    buttons = [
        [
            InlineKeyboardButton(
                'Самовывоз',
                callback_data=self_delivery_callback.to_str()
            ),
            InlineKeyboardButton(
                'Вывоз курьером',
                callback_data=order_delivery_callback.to_str()
            )
        ],
        [
            InlineKeyboardButton(
                'Назад',
                callback_data=CallbackData(CallbackName.MY_ORDERS).to_str()
            )
        ],
    ]

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def signup_keyboard():
    buttons = [
        [
            BUTTONS[ButtonName.CONFIRM_SIGNUP],
            BUTTONS[ButtonName.CHANGE_PERSONAL_DATA]
        ]
    ]

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def my_account(user: dict):
    buttons = []
        
    if user.get('boxes'):
        buttons.append([BUTTONS[ButtonName.MY_ORDERS]])

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def courier_delivery_request():
    buttons = [
        [BUTTONS[ButtonName.COURIER_DELIVERY_YES]]
    ]
    
    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])
    
    return InlineKeyboardMarkup(buttons)


class KeyboardName(Enum):
    MAIN_MENU = auto()
    MY_ACCOUNT = auto()
    TERMS_OF_SERVICE = auto()
    MY_BOX = auto()    
    SELECT_WAREHOUSE = auto()
    ORDER_STORAGE = auto()
    MY_ORDERS = auto()
    BACK_TO_MENU = auto()
    PERSONAL_DATA_AGREEMENT = auto()
    WAREHOUSE = auto()
    SIGN_UP = auto()
    CALL_COURIER = auto()
    CREATE_COURIER_DELIVERY_REQUEST = auto()


keyboards: dict[KeyboardName, callable] = {
    KeyboardName.MAIN_MENU: main_keyboard,
    KeyboardName.TERMS_OF_SERVICE: tos_keyboard,
    KeyboardName.MY_BOX: my_box_keyboard,
    KeyboardName.SELECT_WAREHOUSE: warehouses_keyboard,
    KeyboardName.MY_ORDERS: my_orders_keyboard,
    KeyboardName.ORDER_STORAGE: order_storage_keyboard,
    KeyboardName.BACK_TO_MENU: back_to_menu_keyboard,
    KeyboardName.PERSONAL_DATA_AGREEMENT: ppd_peyboard,
    KeyboardName.CALL_COURIER: call_courirer_keyboard,
    KeyboardName.SIGN_UP: signup_keyboard,
    KeyboardName.MY_ACCOUNT: my_account,
    KeyboardName.CREATE_COURIER_DELIVERY_REQUEST: courier_delivery_request,
}
