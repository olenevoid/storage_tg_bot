from telegram import Update
from ptb import keyboard
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)


MAIN, FAQ, ORDER_STORAGE, MY_SORAGE, STORAGE_LIST, PPD, INPUT_ADDRESS, INPUT_PHONE, FINAL = range(9)

# тут идут наши обработчики
async def start(update, context):
    if 'last_message' in context.user_data:
        await context.user_data['last_message'].delete()
    await update.message.reply_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboard.main_keyboard
    )
    return MAIN


# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update, context):
    await update.message.delete()


async def handle_back_menu(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboard.main_keyboard
    )
    return MAIN


async def handle_faq(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboard.faq_keyboard
    )
    return FAQ


async def handle_order_storage(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Как вы хотите передать вещи на склад?",
        reply_markup=keyboard.order_storage_keyboard
    )
    return ORDER_STORAGE


async def handle_my_orders(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboard.back_to_menu
    )
    return MY_SORAGE


async def handle_self_delivery(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Список складов куда можно обратиться и где есть свободные места",
        reply_markup=keyboard.back_to_menu
    )
    return STORAGE_LIST


async def handle_free_removal(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "тут согласие на обработку данных",
        reply_markup=keyboard.ppd_keyboard
    )
    return PPD


async def validate_address(update, context):
    await update.message.reply_text(
        "Введите номер телефона",
        reply_markup=keyboard.back_to_menu
    )
    return INPUT_PHONE


async def validate_phone(update, context):
    await update.message.reply_text(
        "выводится прайс лист",
        reply_markup=keyboard.call_courier_keyboard
    )
    return FINAL


async def handle_yes(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "ВВедите адрес от куда забрать вещи",
        reply_markup=keyboard.back_to_menu
    )
    return INPUT_ADDRESS


async def handle_final(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "С вами скоро свяжутся",
        reply_markup=keyboard.back_to_menu
    )


def get_handlers():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN: [
                CallbackQueryHandler(handle_faq, 'faq'),
                CallbackQueryHandler(handle_order_storage, 'order_storage'),
                CallbackQueryHandler(handle_my_orders, 'my_orders'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            FAQ: [
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            ORDER_STORAGE: [
                CallbackQueryHandler(handle_self_delivery, 'self_delivery'),
                CallbackQueryHandler(handle_free_removal, 'free_removal'),
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            MY_SORAGE: [
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            STORAGE_LIST: [
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            PPD: [
                CallbackQueryHandler(handle_yes, 'yes'),
                CallbackQueryHandler(handle_back_menu, 'no'),
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            INPUT_ADDRESS: [
                MessageHandler(filters.ALL, validate_address),
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
            ],
            INPUT_PHONE: [
                MessageHandler(filters.ALL, validate_phone),
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
            ],
            FINAL: [
                CallbackQueryHandler(handle_final, 'hand_over_things'),
                CallbackQueryHandler(handle_back_menu, 'back_to_menu'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],                
        },
        fallbacks=[CommandHandler("start", start)],
    )
