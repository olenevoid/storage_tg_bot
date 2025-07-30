from telegram import InlineKeyboardMarkup
from ptb.callbacks import CallbackName, CallbackButton
from django.core.paginator import Page
import ptb.static_buttons as static_buttons


def main_keyboard(client: dict = None):

    buttons = [
        [static_buttons.TOS],
    ]

    if client:
        buttons.append([static_buttons.ORDER_STORAGE])
        buttons.append([static_buttons.MY_ACCOUNT])
    else:
        buttons.append([static_buttons.SHOW_PRICES])
        buttons.append([static_buttons.SIGNUP])

    return InlineKeyboardMarkup(buttons)


def tos_keyboard():
    return InlineKeyboardMarkup(
        [
            [static_buttons.TOS_DOWNLOAD],
            [static_buttons.FAQ],
            [static_buttons.FORBIDDEN],
            [static_buttons.BACK_TO_MENU],
        ]
    )


def back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [static_buttons.BACK_TO_MENU],
        ]
    )


def order_storage_keyboard():
    return InlineKeyboardMarkup(
        [
            [static_buttons.SHOW_PRICES],
            [static_buttons.COURIER_DELIVERY],
            [static_buttons.SELF_DELIVERY],
            [static_buttons.BACK_TO_MENU],
        ]
    )


def ppd_peyboard():
    return InlineKeyboardMarkup(
        [
            [static_buttons.PPD_DOWNLOAD],
            [
                static_buttons.PPD_YES,
                static_buttons.PPD_NO
            ],
        ]
    )


def _get_page_buttons(page: Page, callback_name: CallbackName):
    page_buttons = []

    if page.has_previous():
        page_number = page.previous_page_number()
        previous_page = CallbackButton('<--', callback_name, page=page_number)
        page_buttons.append(previous_page)

    if page.has_next():
        page_number = page.next_page_number()
        next_page = CallbackButton('-->', callback_name, page=page_number)
        page_buttons.append(next_page)

    return page_buttons


def warehouses_keyboard(page: Page):
    buttons = []

    warehouses = page.object_list

    for warehouse in warehouses:

        button = [
            CallbackButton(
                warehouse.get('name'),
                CallbackName.WAREHOUSE,
                id=warehouse.get('id')
            ),
        ]
        buttons.append(button)

    buttons.append(_get_page_buttons(page, CallbackName.SELECT_WAREHOUSE))

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def my_orders_keyboard(page: Page):
    buttons = []

    boxes = page.object_list

    for box in boxes:
        size = box.get('size')

        text = f'Размер {size.get('code')} на {box.get('location')}'

        button = [
            CallbackButton(
                text,
                CallbackName.MY_BOX,
                id=box.get('id')
            )
        ]

        buttons.append(button)

    buttons.append(_get_page_buttons(page, CallbackName.MY_ORDERS))

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def my_box_keyboard(box_id):

    buttons = [
        [
            CallbackButton(
                'Самовывоз',
                CallbackName.OPEN_BOX,
                box_id=box_id
            ),
            CallbackButton(
                'Вывоз курьером',
                CallbackName.ORDER_DELIVERY,
                box_id=box_id
            )
        ],
        [
            CallbackButton('Назад',CallbackName.MY_ORDERS)
        ],
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def signup_keyboard():
    buttons = [
        [
            static_buttons.CONFIRM_SIGNUP,
            static_buttons.CHANGE_PERSONAL_DATA
        ]
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def my_account(user: dict):
    buttons = []

    if user.get('boxes'):
        buttons.append([static_buttons.MY_ORDERS])

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def courier_delivery_request():
    buttons = [
        [static_buttons.COURIER_DELIVERY_YES]
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def select_box(boxes: list[dict]):
    buttons = []

    for box in boxes:
        size = box.get('size')

        button = CallbackButton(
            size.get('code'),
            CallbackName.SELECT_BOX,
            size_id=size.get('id')
        )

        buttons.append([button])

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def promo():
    buttons = [
        [static_buttons.NO_PROMO],
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def confirm_rent():
    buttons = [
        [static_buttons.CONFIRM_RENT]
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def open_box():
    buttons = [
        [static_buttons.OPEN_QR],
        [
            static_buttons.ADD_THINGS,
            static_buttons.REMOVE_THINGS
        ]
    ]

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def remove_items_from_box(box):
    buttons = []
    items = box.get('stored_items')

    for item in items:
        button = CallbackButton(
            item.get('name'),
            CallbackName.REMOVE_ITEM,
            item_id=item.get('id')
        )

        buttons.append(button)

    buttons = _split_to_sublists(buttons)

    back_to_box_button = CallbackButton(
        'Назад',
        CallbackName.MY_BOX,
        id=box.get('id')
    )

    buttons.append([back_to_box_button])

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


# В идеале надо перенести в хэлперы, но я не придумал, что там еще хранить
def _split_to_sublists(items: list, chunk_size: int = 2):
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
