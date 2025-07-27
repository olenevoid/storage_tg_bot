from telegram import Update
from ptb.keyboard import keyboards
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
from ptb.callbacks import State, CallbackData, parse_callback_data_string
import bot_django_app.bot_db as bot_db
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator, Page


PER_PAGE = 2

'''(MAIN, FAQ, ORDER_STORAGE, MY_SORAGE, MY_BOX, STORAGE_LIST, STORAGE_DETAILS, PPD, 
INPUT_ADDRESS, INPUT_PHONE, FINAL) = range(11)'''

# тут идут наши обработчики
async def start(update, context):
    await update.message.delete()
    await update.message.reply_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboards[State.MAIN_MENU]()
    )
    return State.MAIN_MENU


# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update, context):
    await update.message.delete()


async def handle_back_menu(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboards[State.MAIN_MENU]()
    )
    return State.MAIN_MENU


async def handle_faq(update, context):
    await update.callback_query.answer()

    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboards[State.FAQ]()
    )
    return State.FAQ


async def handle_order_storage(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Как вы хотите передать вещи на склад?",
        reply_markup=keyboards[State.ORDER_STORAGE]()
    )
    return State.ORDER_STORAGE


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
        reply_markup=keyboards[State.MY_ORDERS](page)
    )

    return State.MY_ORDERS


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
        reply_markup=keyboards[State.MY_BOX](box_id)
    )

    return State.MY_BOX


async def handle_self_delivery(update, context):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    page_number = params.get('page') or 1

    warehouses = await sync_to_async(bot_db.get_all_warehouses)()
    page: Page = Paginator(warehouses, per_page=PER_PAGE).page(page_number)

    await update.callback_query.edit_message_text(
        "Доступные склады",
        reply_markup=keyboards[State.WAREHOUSES](page)
    )
    return State.WAREHOUSES


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
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )

    return State.WAREHOUSE


async def handle_free_removal(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "тут согласие на обработку данных",
        reply_markup=keyboards[State.PERSONAL_DATA]()
    )
    return State.PERSONAL_DATA


async def validate_address(update, context):
    await update.message.reply_text(
        "Введите номер телефона",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.INPUT_PHONE


async def validate_phone(update, context):
    await update.message.reply_text(
        "выводится прайс лист",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.FINAL


async def handle_yes(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "ВВедите адрес от куда забрать вещи",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.INPUT_ADDRESS


async def handle_final(update, context):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "С вами скоро свяжутся",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )


def get_handlers():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(handle_faq, f'^{State.FAQ.value}*.*'),
                CallbackQueryHandler(handle_order_storage, f'^{State.ORDER_STORAGE.value}*.*'),
                CallbackQueryHandler(handle_my_orders, f'^{State.MY_ORDERS.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.FAQ: [
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.ORDER_STORAGE: [
                CallbackQueryHandler(handle_self_delivery, f'^{State.WAREHOUSES.value}*.*'),
                CallbackQueryHandler(handle_free_removal, f'^{State.FREE_REMOVAL.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.WAREHOUSES: [
                CallbackQueryHandler(handle_self_delivery, f'^{State.WAREHOUSES.value}*.*'),
                CallbackQueryHandler(handle_warehouse, f'^{State.WAREHOUSE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.WAREHOUSE: [
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.MY_ORDERS: [
                CallbackQueryHandler(handle_my_box, f'^{State.MY_BOX.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.MY_BOX: [
                CallbackQueryHandler(handle_my_orders, f'^{State.MY_ORDERS.value}*.*'),
                CallbackQueryHandler(handle_my_box, f'^{State.MY_BOX.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.PERSONAL_DATA: [
                CallbackQueryHandler(handle_yes, f'^{State.PERSONAL_DATA_AGREE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.PERSONAL_DATA_DISAGREE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.INPUT_ADDRESS: [
                MessageHandler(filters.ALL, validate_address),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.INPUT_PHONE: [
                MessageHandler(filters.ALL, validate_phone),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.FINAL: [
                CallbackQueryHandler(handle_final, f'^{State.HAND_OVER_THINGS.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],                
        },
        fallbacks=[CommandHandler("start", start)],
    )
