from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    

def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
            InlineKeyboardButton(
                'Условия хранения/FAQ',
                callback_data='terms_of_service'
            ),
            ],
            [
                InlineKeyboardButton(
                    'Выбрать склад',
                    callback_data='warehouses'
                ),
            ],
            [
                InlineKeyboardButton(
                    'Мои заказы',
                    callback_data='my_orders'
                ),
            ]
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
