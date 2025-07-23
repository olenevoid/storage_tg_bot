from telegram import Update
from telegram.ext import ContextTypes
from keyboards import (main_menu, tos_menu, my_orders, my_box, warehouses_menu,
                       warehouse_menu)
from bot.demo_dataclasses import get_demo_user, get_demo_warehouses, find_warehouse


class ParsedQuery:
    def __init__(self, query_data):
        parsed_query = query_data.split('__')

        value = None
        
        if len(parsed_query) > 1:
            value = int(parsed_query[1])
        
        self.name: str = parsed_query[0]
        self.value: int | None = value


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    text = 'test'
    await update.message.reply_text(text, parse_mode='HTML')
    

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_demo_user()
    text = 'Главное меню'
    await update.message.reply_text(text,
                                    parse_mode='HTML',
                                    reply_markup=main_menu(user)
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    tg_id = str(query.from_user.id)
    user = get_demo_user()
    await query.answer()

    parsed_query = ParsedQuery(query.data)

    if parsed_query.name == 'terms_of_service':
        text = 'Условия хранения/FAQ'
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=tos_menu()
        )

    if parsed_query.name == 'main_menu':
        text = 'Главное меню'
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=main_menu(user)
        )
        
    if parsed_query.name == 'warehouses':
        warehouses = get_demo_warehouses()
        text = ''
        for warehouse in warehouses:
            text += (
                f'Адрес: {warehouse.address}\n'
                f'Свободных ячеек: {warehouse.total}\n'
            )
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=warehouses_menu(warehouses)
        )
    
    if parsed_query.name == 'warehouse':
        warehouse = find_warehouse(parsed_query.value)
        text = (
            f'Адрес: {warehouse.address}\n'
            f'Свободных ячеек 1 куб. м. {warehouse.number_of_1cub_m_boxes}\n'
            f'Свободных ячеек 2 куб. м. {warehouse.number_of_2cub_m_boxes}\n'
            f'Свободных ячеек 3 куб. м. {warehouse.number_of_3cub_m_boxes}\n'
            f'Свободных ячеек 4 куб. м. {warehouse.number_of_4cub_m_boxes}\n'
            '\n'
            'TODO: Тут должны быть кнопки доступных ячеек нужного объема, но т.к. я не сделал списки ячеек внутри склада, сейчас это не реализовать. Проще будет уже с живой моделью\n'
            'Расценки по идее должны быть привязаны к определенным ячейкам определенных складов \n'            
            'И было бы логично уже после выбора ячейки просить согласие на обработку пользовательских данных и вызов курьера'
        )
        
        
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=warehouse_menu(warehouse)
        )
    
    if parsed_query.name == 'my_orders':
        
        text = ''
        
        for box in user.boxes_in_usage:
            line = (
                f'{box.name}\n'
                f'По адресу: {box.address}\n'
                f'До: {box.rented_till.strftime('%Y-%m-%d')}\n'
                '\n'
            )
            text += line
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=my_orders(user)
        )

    if parsed_query.name == 'my_box':        
        box = user.find_box(parsed_query.value)
        
        if box:
            text = (
                f'{box.name}\n'
                f'По адресу: {box.address}\n'
                f'Объем: {box.volume} куб. м.\n'
                f'Высота: {box.height} м.\n'
                f'Ширина: {box.width} м.\n'
                f'Глубина: {box.length} м.\n'
                f'До: {box.rented_till.strftime('%Y-%m-%d')}\n'
                '\n'
                'Предметы на хранении:\n'
            )
            
            for item in box.items_stored:
                text += f'{item}\n'
        else:
            text = 'Ошибка при получении информации о ячейке'
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=my_box(box)
        )
        
    if parsed_query.name == 'extend_time':
        box = user.find_box(parsed_query.value)
        text = f'TODO: Продлеваем время для {box.name}'
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=my_box(box)
        )
    
    if parsed_query.name == 'selfpick':
        box = user.find_box(parsed_query.value)
        text = f'TODO: Самовывоз по QR из {box.name}'
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=my_box(box)
        )
    
    if parsed_query.name == 'home_delivery':
        box = user.find_box(parsed_query.value)
        text = f'TODO: Заказываем доставку домой из {box.name}'
        
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=my_box(box)
        )

    if parsed_query.name == 'terms':
        text = 'Правила пользования сервисом'
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=tos_menu()
        )

    if parsed_query.name == 'faq':
        text = 'Часто задаваемые вопросы'
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=tos_menu()
        )

    if parsed_query.name == 'forbidden':
        text = 'Запрещенные к хранению вещи'
        await query.edit_message_text(text,
                                      parse_mode='HTML',
                                      reply_markup=tos_menu()
        )


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update.update_id} caused error {context.error}')
