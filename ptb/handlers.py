from telegram import Update
from ptb import keyboard
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from ptb.callbacks import CallbackName, CallbackData, parse_callback_data_string
import bot_django_app.bot_db as bot_db
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator, Page


PER_PAGE = 2

(MAIN, FAQ, ORDER_STORAGE, MY_SORAGE, MY_BOX, STORAGE_LIST, STORAGE_DETAILS, PPD, 
INPUT_ADDRESS, INPUT_PHONE, FINAL) = range(11)

# тут идут наши обработчики
async def start(update, context):
    await update.message.delete()
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
    params = parse_callback_data_string(update.callback_query.data).params
    test_tg = 100000001
    client_tg = test_tg  # update.callback_query.from_user.id

    page_number = params.get('page') or 1

    boxes = await sync_to_async(bot_db.get_all_boxes_for_user)(client_tg)

    page = Paginator(boxes, per_page=2).page(page_number)

    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboard.get_my_orders_keyboard(page)
    )

    return MY_SORAGE


async def handle_my_box(update: Update, context):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    box_id = params.get('id')
    box = await sync_to_async(bot_db.get_box)(box_id)

    text = (
        f'Размер ячейки: {box.get('size')}\n'
        f'Адрес склада: {box.get('address')}\n'
        f'Арендована до: {box.get('rented_until')}\n'
        f'Предметы на хранении:\n'
    )

    for item in box.get('stored_items'):
        text += f'{item}\n'

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboard.get_my_box_keyboard(box_id)
    )

    return MY_BOX


async def handle_self_delivery(update, context):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    page_number = params.get('page') or 1

    warehouses = await sync_to_async(bot_db.get_all_warehouses)()
    page: Page = Paginator(warehouses, per_page=PER_PAGE).page(page_number)

    kb = keyboard.get_warehouse_keyboard(page)
    await update.callback_query.edit_message_text(
        "Доступные склады",
        reply_markup=kb
    )
    return STORAGE_LIST


async def handle_warehouse(update, context):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
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

    return STORAGE_DETAILS


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
                CallbackQueryHandler(handle_faq, f'^{CallbackName.FAQ.value}*.*'),
                CallbackQueryHandler(handle_order_storage, f'^{CallbackName.ORDER_STORAGE.value}*.*'),
                CallbackQueryHandler(handle_my_orders, f'^{CallbackName.MY_ORDERS.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            FAQ: [
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            ORDER_STORAGE: [
                CallbackQueryHandler(handle_self_delivery, f'^{CallbackName.SELF_DELIVERY.value}*.*'),
                CallbackQueryHandler(handle_free_removal, f'^{CallbackName.FREE_REMOVAL.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            STORAGE_LIST: [
                CallbackQueryHandler(handle_self_delivery, f'^{CallbackName.SELF_DELIVERY.value}*.*'),
                CallbackQueryHandler(handle_warehouse, f'^{CallbackName.WAREHOUSE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            STORAGE_DETAILS: [
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
            ],
            MY_SORAGE: [
                CallbackQueryHandler(handle_my_box, f'^{CallbackName.MY_BOX.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            MY_BOX: [
                CallbackQueryHandler(handle_my_orders, f'^{CallbackName.MY_ORDERS.value}*.*'),
                CallbackQueryHandler(handle_my_box, f'^{CallbackName.MY_BOX.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
            ],
            PPD: [
                CallbackQueryHandler(handle_yes, f'^{CallbackName.PERSONAL_DATA_AGREE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.PERSONAL_DATA_DISAGREE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            INPUT_ADDRESS: [
                MessageHandler(filters.ALL, validate_address),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
            ],
            INPUT_PHONE: [
                MessageHandler(filters.ALL, validate_phone),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
            ],
            FINAL: [
                CallbackQueryHandler(handle_final, f'^{CallbackName.HAND_OVER_THINGS.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{CallbackName.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],                
        },
        fallbacks=[CommandHandler("start", start)],
    )