from telegram import Update
from ptb import keyboard
from telegram.ext import (
    filters,
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
)
from ptb.callbacks import parse_callback_data_string, CallbackName
import bot_django_app.bot_db as bot_db
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator, Page


HANDLERS = {}


# создаем декоратор @register_callback()
def register_callback(callback_name: CallbackName):
    def decorator(function):
        HANDLERS[callback_name] = function
        return function
    return decorator


# тут идут наши обработчики
async def start(update, context):
    await update.message.reply_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboard.get_keyboard('main')
    )


# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update, context, params):
    await update.message.delete()


@register_callback(CallbackName.FAQ)
async def handle_FAQ(update, context, params):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboard.get_keyboard('faq')
    )


@register_callback(CallbackName.ORDER_STORAGE)
async def handle_order_storage(update, context, params: dict):
    page_number = params.get('page') or 1

    warehouses = await sync_to_async(bot_db.get_all_warehouses)()
    page: Page = Paginator(warehouses, per_page=1).page(page_number)

    kb = keyboard.get_warehouse_keyboard(page)
    await update.callback_query.edit_message_text(
        "Доступные склады",
        reply_markup=kb
    )


@register_callback(CallbackName.WAREHOUSE)
async def handle_warehouse(update, context, params: dict):
    warehouse = await sync_to_async(bot_db.get_warehouse)(params.get('id'))

    has_delivery_text = 'Нет'

    if warehouse.has_delivery:
        has_delivery_text = 'Да'

    text = (
        f'Название: {warehouse.name}\n'
        f'Адрес: {warehouse.address}\n'
        f'Есть доставка: {has_delivery_text}\n'
    )

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboard.get_keyboard('unknown_cmd')
    )


@register_callback(CallbackName.MY_ORDERS)
async def handle_my_orders(update, context, params):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboard.get_keyboard('my_orders')
    )


@register_callback(CallbackName.MAIN_MENU)
async def handle_main_menu(update, context, params):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "hi",
        reply_markup=keyboard.get_keyboard('main')
    )


# Функция берет наш callback_data как ключ и ищет по нему функцию для обработки
async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    callback_data = parse_callback_data_string(query.data)
    handler = HANDLERS.get(callback_data.name)
    if handler:
        await handler(update, context, callback_data.params)
    else:
        await query.edit_message_text(
            "Неизвестная команда",
            reply_markup=keyboard.get_keyboard('unknown_cmd')
        )


# Возвращает все обработчики для регистрации в приложении бота
def get_handlers():
    handlers = [
        CommandHandler('start', start),
        MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
        CallbackQueryHandler(callback_handler),
    ]
    return handlers
