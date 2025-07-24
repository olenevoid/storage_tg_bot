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


HANDLERS = {}
# создаем декоратор @register_callback()
def register_callback(callback_data):
    def decorator(function):
        HANDLERS[callback_data] = function
        return function
    return decorator

# тут идут наши обработчики
async def start(update, context):
    await update.message.reply_text(
        "hi",
        reply_markup=keyboard.get_keyboard('main')
    )
    
# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update, context):
    await update.message.delete()


@register_callback('faq')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboard.get_keyboard('faq')
    )
    
    
@register_callback('order_storage')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Как вы хотите передать вещи на склад?",
        reply_markup=keyboard.get_keyboard('order_storage')
    )
    

@register_callback('my_orders')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboard.get_keyboard('my_orders')
    )
    

@register_callback('back_to_menu')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "hi",
        reply_markup=keyboard.get_keyboard('main')
    )
    
# Функция берет наш callback_data как ключ и ищет по нему функцию для обработки
async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    handler = HANDLERS.get(query.data)
    if handler:
        await handler(update, context)
    else:
        await query.edit_message_text(
            "Неизвестная команда",
            reply_markup=keyboard.get_keyboard('unknown_cmd')
        )
        
# Возвращает все обработчики для регистрации в приложении бота
def get_handlers():
    handlers = [
        CommandHandler('start', start),
        MessageHandler( filters.Regex(r'^(?!\/start).*'), unknown_cmd),
        CallbackQueryHandler(callback_handler),
    ]
    return handlers
