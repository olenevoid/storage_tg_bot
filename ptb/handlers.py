from telegram import Update
from ptb.keyboards import keyboards
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext
)
from ptb.callbacks import State, parse_callback_data_string
import bot_django_app.bot_db as bot_db
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator, Page
from ptb import validators


PER_PAGE = 2


# тут идут наши обработчики
async def start(update: Update, context: CallbackContext):
    await update.message.delete()
    telegram_id = update.message.from_user.id
    client = await sync_to_async(bot_db.find_client_by_tg)(telegram_id)

    await update.message.reply_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboards[State.MAIN_MENU](client)
    )
    return State.MAIN_MENU


# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update: Update, context: CallbackContext):
    await update.message.delete()


async def handle_back_menu(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    telegram_id = update.callback_query.from_user.id
    client = await sync_to_async(bot_db.find_client_by_tg)(telegram_id)

    await update.callback_query.edit_message_text(
        "много примеров, когда аренда склада может пригодиться",
        reply_markup=keyboards[State.MAIN_MENU](client)
    )
    return State.MAIN_MENU


async def handle_faq(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    await update.callback_query.edit_message_text(
        "Условия хранения/FAQ",
        reply_markup=keyboards[State.FAQ]()
    )
    return State.FAQ


async def handle_order_storage(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Как вы хотите передать вещи на склад?",
        reply_markup=keyboards[State.ORDER_STORAGE]()
    )
    return State.ORDER_STORAGE


async def handle_my_orders(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    telegram_id = update.callback_query.from_user.id

    page_number = params.get('page') or 1

    boxes = await sync_to_async(bot_db.get_all_boxes_for_client)(client_tg)

    page = Paginator(boxes, per_page=2).page(page_number)

    await update.callback_query.edit_message_text(
        "Мои заказы",
        reply_markup=keyboards[State.MY_ORDERS](page)
    )

    return State.MY_ORDERS


async def handle_my_box(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    box_id = params.get('id')
    box = await sync_to_async(bot_db.get_box)(box_id)
    box_size = box.get('size')

    text = (
        f'Размер ячейки: {box_size.get('code')}\n'
        f'Цена в месяц: {box_size.get('price')}\n'
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


async def handle_self_delivery(update: Update, context: CallbackContext):
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


async def handle_warehouse(update: Update, context: CallbackContext):
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


async def handle_personal_data_agreement(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "тут согласие на обработку данных",
        reply_markup=keyboards[State.PERSONAL_DATA_AGREEMENT]()
    )
    return State.PERSONAL_DATA_AGREEMENT


async def validate_address(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Введите номер телефона",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.FINAL


async def handle_input_name(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Введите ФИО",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.INPUT_FULL_NAME


async def validate_full_name(update: Update, context: CallbackContext):
    name = update.message.text

    if validators.name_is_valid(name):
        text = f'Вы ввели корректное {name}, теперь введите телефон'
        state = State.INPUT_PHONE
        context.user_data['full_name'] = name
    else:
        text = f'Вы ввели некорректное имя {name}, попробуйте еще раз'
        state = State.INPUT_FULL_NAME

    await update.message.reply_text(
        text,
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return state


async def validate_phone(update: Update, context: CallbackContext):
    phone = update.message.text

    if validators.phone_is_valid(phone):
        text = f'Вы ввели корректный телефон {phone}, теперь введите имейл'
        state = State.INPUT_EMAIL
        context.user_data['phone'] = phone
    else:
        text = f'Вы ввели некорректный телефон {phone}, попробуйте еще раз'
        state = State.INPUT_PHONE

    await update.message.reply_text(
        text,
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return state


async def validate_email(update: Update, context: CallbackContext):
    email = update.message.text

    if validators.email_is_valid(email):
        context.user_data['email'] = email
        text = (
            'Введенные данные корректны?\n'
            f'Имя: {context.user_data['full_name']}\n'
            f'Телефон: {context.user_data['phone']}\n'
            f'Имейл: {context.user_data['email']}\n'
        )
        state = State.SIGN_UP
        keyboard = keyboards[State.SIGN_UP]()

    else:
        text = f'Вы ввели некорректный имейл {email}, попробуйте еще раз'
        state = State.INPUT_EMAIL
        keyboard = keyboards[State.BACK_TO_MENU]()

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )

    return state


async def handle_signup(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = (
        'Пользователь зарегистрирован\n'
        f'Имя: {context.user_data['full_name']}\n'
        f'Телефон: {context.user_data['phone']}\n'
        f'Имейл: {context.user_data['email']}\n'
    )

    client = {
        'full_name': context.user_data['full_name'],
        'phone': context.user_data['phone'],
        'email': context.user_data['email'],
        'telegram_id': update.callback_query.from_user.id
    }

    await bot_db.acreate_client(client)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.SIGN_UP


async def handle_yes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "ВВедите адрес от куда забрать вещи",
        reply_markup=keyboards[State.BACK_TO_MENU]()
    )
    return State.INPUT_ADDRESS


async def handle_final(update: Update, context: CallbackContext):
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
                CallbackQueryHandler(handle_personal_data_agreement, f'^{State.PERSONAL_DATA_AGREEMENT.value}*.*'),
                CallbackQueryHandler(handle_my_orders, f'^{State.MY_ORDERS.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.FAQ: [
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.ORDER_STORAGE: [
                CallbackQueryHandler(handle_self_delivery, f'^{State.WAREHOUSES.value}*.*'),                
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
            State.INPUT_ADDRESS: [
                MessageHandler(filters.ALL, validate_address),
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
            State.PERSONAL_DATA_AGREEMENT: [
                CallbackQueryHandler(handle_input_name, f'^{State.INPUT_FULL_NAME.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.PERSONAL_DATA_DISAGREE.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.INPUT_FULL_NAME: [
                MessageHandler(filters.ALL, validate_full_name),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.INPUT_PHONE: [
                MessageHandler(filters.ALL, validate_phone),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.INPUT_EMAIL: [
                MessageHandler(filters.ALL, validate_email),
                CallbackQueryHandler(handle_signup, f'^{State.SIGN_UP.value}*.*'),
                CallbackQueryHandler(handle_back_menu, f'^{State.MAIN_MENU.value}*.*'),
            ],
            State.SIGN_UP: [
                CallbackQueryHandler(handle_signup, f'^{State.SIGN_UP.value}*.*'),
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
