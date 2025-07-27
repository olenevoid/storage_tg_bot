from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, State
from django.core.paginator import Page


# Все кнопки бота. Нажатия регестрируются через callback_data
# в файле handlers.py
btns = {
    'faq': InlineKeyboardButton(
        'Условия хранения/FAQ',
        callback_data=CallbackData(State.TERMS_OF_SERVICE).to_str()
    ),
    'order_storage': InlineKeyboardButton(
        'Выбрать склад',
        callback_data=CallbackData(State.ORDER_STORAGE).to_str()
    ),
    'my_orders': InlineKeyboardButton(
        'Мои заказы',
        callback_data=CallbackData(State.MY_ORDERS).to_str()
    ),
    'tos_download': InlineKeyboardButton(
        'Скачать условия',
        callback_data=CallbackData(State.DOWNLOAD_TOS).to_str()
    ),
    'back_to_menu': InlineKeyboardButton(
        'В главное меню',
        callback_data=CallbackData(State.MAIN_MENU).to_str()
    ),
    'forbidden': InlineKeyboardButton(
        'Запрещенные к хранению вещества',
        callback_data=CallbackData(State.FORBIDDEN_TO_STORE).to_str()
    ),
    'back': InlineKeyboardButton('назад', callback_data='back'),
    'free_removal': InlineKeyboardButton('Бесплатный вывоз', callback_data='free_removal'),
    'self_delivery': InlineKeyboardButton('Доставлю сам', callback_data='self_delivery'),
    'yes': InlineKeyboardButton(
        'Да',
        callback_data=CallbackData(State.INPUT_FULL_NAME).to_str()
    ),
    'no': InlineKeyboardButton(
        'Нет (назад в меню)',
        callback_data=CallbackData(State.MAIN_MENU).to_str()
        ),
    'hand_over_things': InlineKeyboardButton('Сдать вещи', callback_data='hand_over_things'),
    'signup': InlineKeyboardButton(
        'Зарегистрироваться',
        callback_data=CallbackData(State.PERSONAL_DATA_AGREEMENT).to_str()
    ),
    'confirm_signup': InlineKeyboardButton(
        'Подтвердить регистрацию',
        callback_data=CallbackData(State.SIGN_UP).to_str()
    ),
    'change_personal_data': InlineKeyboardButton(
        'Ввести данные заново',
        callback_data=CallbackData(State.PERSONAL_DATA_AGREEMENT).to_str()
    )
}


# Ниже создаем клавиатуры из кнопок
def main_keyboard(client: dict = None):

    buttons = [
        [btns['faq']],        
        [btns['order_storage']],
    ]

    if client:
        buttons.append([btns['my_orders']])
    else:
        buttons.append([btns['signup']])

    return InlineKeyboardMarkup(buttons)


def tos_keyboard():
    return InlineKeyboardMarkup(
        [
            [btns['tos_download']],
            [btns['faq']],
            [btns['forbidden']],
            [btns['back_to_menu']],
        ]
    )


def back_to_menu_keyboard():
    return InlineKeyboardMarkup(
        [
            [btns['back_to_menu']],
        ]
    )


def order_storage_keyboard():
    return InlineKeyboardMarkup(
        [
            [btns['free_removal']],
            [btns['self_delivery']],
            [btns['back_to_menu']],
        ]
    )


def ppd_peyboard():
    return InlineKeyboardMarkup(
        [
            [btns['yes']],
            [btns['no']],
        ]
    )


def call_courirer_keyboard():
    return InlineKeyboardMarkup(
        [
            [btns['hand_over_things']],
            [btns['back_to_menu']],
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

    buttons.append([btns['back_to_menu']])

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

    buttons.append([btns['back_to_menu']])

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

    buttons.append([btns['back_to_menu']])

    return InlineKeyboardMarkup(buttons)


def signup_keyboard():
    buttons = [
        [
            btns['confirm_signup'],
            btns['change_personal_data']
        ]
    ]

    buttons.append([btns['back_to_menu']])

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
