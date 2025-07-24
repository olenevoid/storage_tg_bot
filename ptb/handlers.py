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

def register_callback(callback_data):
    def decorator(function):
        HANDLERS[callback_data] = function
        return function
    return decorator


async def start(update, context):
    await update.message.reply_text("hi",
        reply_markup=keyboard.main_keyboard()
    )


@register_callback('terms_of_service')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboard.main_keyboard()
    )
    
    
@register_callback('warehouses')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбрать склад",
        reply_markup=keyboard.main_keyboard()
    )
    

@register_callback('my_orders')
async def handle_button(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboard.main_keyboard()
    )
    

async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    handler = HANDLERS.get(query.data)
    if handler:
        await handler(update, context)
    else:
        await query.edit_message_text("Неизвестная команда")
        
def get_handlers():
    handlers = [
        CommandHandler('start', start),
        CallbackQueryHandler(callback_handler),
    ]
    return handlers
