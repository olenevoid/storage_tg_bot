from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, CallbackName
from django.core.paginator import Page
import ptb.static_buttons as static_buttons
from enum import Enum, auto


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

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def my_orders_keyboard(page: Page):
    buttons = []

    boxes = page.object_list

    for box in boxes:
        size = box.get('size')
        callback_data = CallbackData(
            CallbackName.MY_BOX,
            {'id': box.get('id')}
        )

        text = f'Размер {size.get('code')} на {box.get('location')}'

        button = [
            InlineKeyboardButton(
                text,
                callback_data=callback_data.to_str()
            )
        ]

        buttons.append(button)

    buttons.append(_get_page_buttons(page, CallbackName.MY_ORDERS))

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


def my_box_keyboard(box_id):

    self_delivery_callback = CallbackData(
        CallbackName.OPEN_BOX,
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
        callback_data = CallbackData(
            CallbackName.SELECT_BOX,
            {'size_id': size.get('id')}
        )

        button = InlineKeyboardButton(
            size.get('code'),
            callback_data=callback_data.to_str()
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
        item_callback_data = CallbackData(
            CallbackName.REMOVE_ITEM,
            {'item_id': item.get('id')}
        )
        button = InlineKeyboardButton(
            item.get('name'),
            callback_data=item_callback_data.to_str()
        )

        buttons.append(button)

    buttons = _split_to_sublists(buttons)

    box_callback_data = CallbackData(
        CallbackName.MY_BOX,
        {'id': box.get('id')}
    )

    back_to_box_button = InlineKeyboardButton(
        'Назад',
        callback_data=box_callback_data.to_str()
    )

    buttons.append([back_to_box_button])

    buttons.append([static_buttons.BACK_TO_MENU])

    return InlineKeyboardMarkup(buttons)


# В идеале надо перенести в хэлперы, но я не придумал, что там еще хранить
def _split_to_sublists(items: list, chunk_size: int = 2):
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


class KeyboardName(Enum):
    MAIN_MENU = auto()
    MY_ACCOUNT = auto()
    TERMS_OF_SERVICE = auto()
    MY_BOX = auto()
    SELECT_WAREHOUSE = auto()
    SELECT_BOX = auto()
    ORDER_STORAGE = auto()
    MY_ORDERS = auto()
    BACK_TO_MENU = auto()
    PERSONAL_DATA_AGREEMENT = auto()
    WAREHOUSE = auto()
    SIGN_UP = auto()
    CREATE_COURIER_DELIVERY_REQUEST = auto()
    PROMO = auto()
    CONFIRM_RENT = auto()
    OPEN_BOX = auto()
    REMOVE_ITEMS_FROM_BOX = auto()


keyboards: dict[KeyboardName, callable] = {
    KeyboardName.MAIN_MENU: main_keyboard,
    KeyboardName.TERMS_OF_SERVICE: tos_keyboard,
    KeyboardName.MY_BOX: my_box_keyboard,
    KeyboardName.SELECT_WAREHOUSE: warehouses_keyboard,
    KeyboardName.MY_ORDERS: my_orders_keyboard,
    KeyboardName.ORDER_STORAGE: order_storage_keyboard,
    KeyboardName.BACK_TO_MENU: back_to_menu_keyboard,
    KeyboardName.PERSONAL_DATA_AGREEMENT: ppd_peyboard,
    KeyboardName.SIGN_UP: signup_keyboard,
    KeyboardName.MY_ACCOUNT: my_account,
    KeyboardName.CREATE_COURIER_DELIVERY_REQUEST: courier_delivery_request,
    KeyboardName.SELECT_BOX: select_box,
    KeyboardName.PROMO: promo,
    KeyboardName.CONFIRM_RENT: confirm_rent,
    KeyboardName.OPEN_BOX: open_box,
    KeyboardName.REMOVE_ITEMS_FROM_BOX: remove_items_from_box
}
