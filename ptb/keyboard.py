from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, CallbackName
from django.core.paginator import Page


# Все кнопки бота. Нажатия регестрируются через callback_data
# в файле handlers.py
btns = {
    'faq': InlineKeyboardButton(
        'Условия хранения/FAQ',
        callback_data=CallbackData(CallbackName.FAQ).to_str()
    ),
    'order_storage': InlineKeyboardButton(
        'Выбрать склад',
        callback_data=CallbackData(CallbackName.ORDER_STORAGE).to_str()
    ),
    'my_orders': InlineKeyboardButton(
        'Мои заказы',
        callback_data=CallbackData(CallbackName.MY_ORDERS).to_str()
    ),
    'back_to_menu': InlineKeyboardButton(
        'В главное меню',
        callback_data=CallbackData(CallbackName.MAIN_MENU).to_str()
    ),
    'back': InlineKeyboardButton('назад', callback_data='back'),
    'free_removal': InlineKeyboardButton('Бесплатный вывоз', callback_data='free_removal'),
    'self_delivery': InlineKeyboardButton('Доставлю сам', callback_data='self_delivery'),
    'yes': InlineKeyboardButton('Принимаю опд', callback_data='yes'),
    'no': InlineKeyboardButton('Не принимаю опд', callback_data='no'),
    'hand_over_things': InlineKeyboardButton('Сдать вещи', callback_data='hand_over_things'),
    'no': InlineKeyboardButton('Не принимаю опд', callback_data='no'),
    'ok': InlineKeyboardButton('ОК', callback_data='ok'),
}

# Ниже создаем клавиатуры из кнопок
main_keyboard = InlineKeyboardMarkup(
    [
        [btns['faq']],
        [btns['order_storage']],
        [btns['my_orders']],
    ]
)


faq_keyboard = InlineKeyboardMarkup(
    [        
        [btns['back_to_menu']],
    ]
)


back_to_menu = InlineKeyboardMarkup(
    [        
        [btns['back_to_menu']],
    ]
)


order_storage_keyboard = InlineKeyboardMarkup(
    [
        [btns['free_removal']],
        [btns['self_delivery']],
        [btns['back_to_menu']],
    ]
)


my_orders_keyboard = InlineKeyboardMarkup(
    [
        [btns['back_to_menu']],
    ]
)


ppd_keyboard = InlineKeyboardMarkup(
    [
        [btns['yes']],
        [btns['no']],
    ]
)


call_courier_keyboard = InlineKeyboardMarkup(
    [
        [btns['hand_over_things']],
        [btns['back_to_menu']],
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


def get_warehouse_keyboard(page: Page):
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

    buttons.append(_get_page_buttons(page, CallbackName.ORDER_STORAGE))

    buttons.append([btns['back_to_menu']])

    return InlineKeyboardMarkup(buttons)


def get_my_orders_keyboard(page: Page):
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

    buttons.append([btns['back_to_menu']])

    return InlineKeyboardMarkup(buttons)


def get_my_box_keyboard(box_id):

    self_delivery_callback = CallbackData(
        CallbackName.SELF_DELIVERY,
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

    buttons.append([btns['back_to_menu']])

    return InlineKeyboardMarkup(buttons)


# Тут создаем словарь, состояние = клавиатура
keyboards = {
    'main': main_keyboard,
    'faq': faq_keyboard,
    'order_storage': order_storage_keyboard,
    'my_orders': my_orders_keyboard,
    'unknown_cmd': back_to_menu,
    'call_courier': call_courier_keyboard,
    'ppd_keyboard': ppd_keyboard,
}

# Возвращает клавиатуру в зависимости от состояния
def get_keyboard(state: str):
    return keyboards[state]


# def warehouses_menu(warehouses: list[Warehouse]) -> InlineKeyboardMarkup:
    
#     buttons = []
    
#     for warehouse in warehouses:
#         button = [
#             InlineKeyboardButton(
#                 warehouse.address,
#                 callback_data=f'warehouse__{warehouse.id}'
#             )
#         ]
#         buttons.append(button)
    
#     main_menu = [
#         InlineKeyboardButton('Назад', callback_data='main_menu'),
#     ]
    
#     buttons.append(main_menu)
    
#     return InlineKeyboardMarkup(buttons)


# def warehouse_menu(warehouse: Warehouse) -> InlineKeyboardMarkup:
    
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 'Назад',
#                 callback_data='warehouses'
#             ),
#         ]
#     ]
    
#     return InlineKeyboardMarkup(buttons)


# def tos_menu() -> InlineKeyboardMarkup:
    
#     buttons = [
#         [
#             InlineKeyboardButton('Условия хранения', callback_data='terms'),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Часто задаваемые вопросы',
#                 callback_data='faq'
#             ),
#         ],
#         [
#             InlineKeyboardButton(
#                 'Запрещенные к хранению вещи',
#                 callback_data='forbidden'
#             ),
#         ],
#         [
#             InlineKeyboardButton('Назад', callback_data='main_menu'),
#         ],
#     ]
    
#     return InlineKeyboardMarkup(buttons)


# def my_orders(user: User) -> InlineKeyboardMarkup:
#     buttons = []
    
#     for box in user.boxes_in_usage:
#         box_button = [
#             InlineKeyboardButton(
#                 f'{box.name} в {box.address}',
#                 callback_data=f'my_box__{box.id}'
#             )
#         ]
#         buttons.append(box_button)

#     main_menu = [
#             InlineKeyboardButton(
#                 'Назад',
#                 callback_data='main_menu'
#             ),
#         ]
    
#     buttons.append(main_menu)
    
#     return InlineKeyboardMarkup(buttons)


# def my_box(box: Box) -> InlineKeyboardMarkup:
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 'Продлить',
#                 callback_data=f'extend_time__{box.id}'
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 'Забрать (самовывоз)',
#                 callback_data=f'selfpick__{box.id}'
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 'Заказать доставку на дом',
#                 callback_data=f'home_delivery__{box.id}'
#             )
#         ],
#         [
#             InlineKeyboardButton(
#                 'Назад',
#                 callback_data='my_orders'
#             ),
#         ]
#     ]
    
    
#     return InlineKeyboardMarkup(buttons)
