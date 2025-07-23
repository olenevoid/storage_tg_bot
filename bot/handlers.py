from telegram import Update
from bot import keyboard
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
    await update.message.reply_text(
        reply_markup=keyboard.get_test1_keyboard()
    )


@register_callback('button_1')
async def handle_button_1(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Вы нажали кнопку 1!")
    
    
@register_callback('button_2')
async def handle_button_2(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Вы нажали кнопку 2!")
    

async def callback_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    handler = HANDLERS.get(query.data)
    if handler:
        await handler(update, context)
    else:
        await query.edit_message_text("Jib,rf")