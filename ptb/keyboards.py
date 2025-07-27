from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, State
from django.core.paginator import Page
from ptb.buttons import BUTTONS, ButtonName


def main_keyboard(client: dict = None):

    buttons = [
        [BUTTONS[ButtonName.TOS]],
        [BUTTONS[ButtonName.ORDER_STORAGE]],
    ]

    if client:
        buttons.append([BUTTONS[ButtonName.MY_ORDERS]])
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


def _get_page_buttons(page: Page, callback_name: State):
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
            State.WAREHOUSE,
            {'id': warehouse.get('id')}
        )

        button = [
            InlineKeyboardButton(
                warehouse.get('name'),
                callback_data=callback_data.to_str()
            ),
        ]
        buttons.append(button)

    buttons.append(_get_page_buttons(page, State.WAREHOUSES))

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def my_orders_keyboard(page: Page):
    buttons = []

    boxes = page.object_list

    for box in boxes:
        callback_data = CallbackData(
            State.MY_BOX,
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

    buttons.append(_get_page_buttons(page, State.MY_ORDERS))

    buttons.append([BUTTONS[ButtonName.BACK_TO_MENU]])

    return InlineKeyboardMarkup(buttons)


def my_box_keyboard(box_id):

    self_delivery_callback = CallbackData(
        State.WAREHOUSES,
        {'box_id': box_id}
    )

    order_delivery_callback = CallbackData(
        State.ORDER_DELIVERY,
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
                callback_data=CallbackData(State.MY_ORDERS).to_str()
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


keyboards = {
    State.MAIN_MENU: main_keyboard,
    State.TERMS_OF_SERVICE: tos_keyboard,
    State.MY_BOX: my_box_keyboard,
    State.WAREHOUSES: warehouses_keyboard,
    State.MY_ORDERS: my_orders_keyboard,
    State.ORDER_STORAGE: order_storage_keyboard,
    State.BACK_TO_MENU: back_to_menu_keyboard,
    State.PERSONAL_DATA_AGREEMENT: ppd_peyboard,
    State.CALL_COURIER: call_courirer_keyboard,
    State.SIGN_UP: signup_keyboard,
}
