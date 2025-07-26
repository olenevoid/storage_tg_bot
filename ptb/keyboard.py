from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ptb.callbacks import CallbackData, CallbackName

# Все кнопки бота. Нажатия регестрируются через callback_data
# в файле handlers.py
btns = {
    'faq': InlineKeyboardButton(
        'Условия хранения/FAQ',
        callback_data='faq'
    ),
    'order_storage': InlineKeyboardButton(
        'Выбрать склад',
        callback_data='order_storage'
    ),
    'my_orders': InlineKeyboardButton(
        'Мои заказы',
        callback_data='my_orders'
    ),
    'back_to_menu': InlineKeyboardButton(
        'В главное меню',
        callback_data='back_to_menu'
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
