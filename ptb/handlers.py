from telegram import Update
import ptb.keyboards as keyboards
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext
)
from ptb.callbacks import CallbackName, parse_callback_data_string, get_pattern
import bot_django_app.bot_db as bot_db
from asgiref.sync import sync_to_async
from django.core.paginator import Paginator, Page
from ptb import validators
import ptb.strings as strings
from bot_core.settings import BASE_DIR
from os import path
import ptb.settings as settings
from ptb.settings import State


# тут идут наши обработчики
async def start(update: Update, context: CallbackContext):
    await update.message.delete()
    telegram_id = update.message.from_user.id
    user = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    await update.message.reply_text(
        strings.get_main_menu(user),
        reply_markup=keyboards.main_keyboard(user),
        parse_mode='HTML'
    )
    return State.MAIN_MENU


# штука для того чтобы пользователь не мусорил в чате
async def unknown_cmd(update: Update, context: CallbackContext):
    await update.message.delete()


async def handle_back_menu(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    
    # Очищаем сохраненные пользовательские данные при возвращении в меню
    context.user_data.clear()
    
    telegram_id = update.callback_query.from_user.id
    user = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    await update.callback_query.edit_message_text(
        strings.get_main_menu(user),
        reply_markup=keyboards.main_keyboard(user)
    )
    return State.MAIN_MENU


async def handle_my_account(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    telegram_id = update.callback_query.from_user.id
    user = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    text = strings.get_user_details(user)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.my_account(user),
        parse_mode='HTML'
    )
    return State.MY_ACCOUNT


async def handle_tos(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    await update.callback_query.edit_message_text(
        strings.TOS,
        reply_markup=keyboards.tos_keyboard(),
        parse_mode='HTML'
    )
    return State.TERMS_OF_SERVICE


async def handle_download_tos(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    tos_path = path.join(BASE_DIR, f'{settings.STATIC}/tos.pdf')
    with open(tos_path, 'rb') as file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file
        )
    return State.TERMS_OF_SERVICE


async def handle_download_ppd(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    tos_path = path.join(BASE_DIR, f'{settings.STATIC}/ppd.pdf')
    with open(tos_path, 'rb') as file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file
        )
    return State.PERSONAL_DATA_AGREEMENT


async def handle_faq(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    await update.callback_query.edit_message_text(
        strings.FAQ,
        reply_markup=keyboards.tos_keyboard(),
        parse_mode='HTML'
    )
    return State.TERMS_OF_SERVICE


async def handle_forbidden(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    await update.callback_query.edit_message_text(
        strings.FORBIDDEN,
        reply_markup=keyboards.tos_keyboard(),
        parse_mode='HTML'
    )
    return State.TERMS_OF_SERVICE


async def handle_order_storage(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        strings.ORDER_STORAGE,
        reply_markup=keyboards.order_storage_keyboard(),
        parse_mode='HTML'
    )
    return State.ORDER_STORAGE


async def handle_show_prices(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    telegram_id = update.callback_query.from_user.id
    client = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    sizes = await sync_to_async(bot_db.get_all_sizes)()

    text = strings.get_sizes_with_details(sizes)
    if client:
        keyboard = keyboards.order_storage_keyboard()
    else:
        keyboard = keyboards.back_to_menu_keyboard()

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    return State.ORDER_STORAGE


async def handle_my_orders(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    telegram_id = update.callback_query.from_user.id

    page_number = params.get('page') or 1

    client = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    boxes = client.get('boxes')

    page = Paginator(boxes, per_page=2).page(page_number)

    await update.callback_query.edit_message_text(
        strings.MY_BOXES,
        reply_markup=keyboards.my_orders_keyboard(page),
        parse_mode='HTML'
    )

    return State.MY_ORDERS


async def handle_my_box(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    box_id = params.get('id')
    context.user_data['box_id'] = box_id
    box = await sync_to_async(bot_db.get_box)(box_id)
    text = strings.get_box_details(box)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.my_box_keyboard(box_id),
        parse_mode='HTML'
    )

    return State.MY_BOX


async def handle_open_box(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    
    box_id = context.user_data['box_id']
    
    box = await sync_to_async(bot_db.get_box)(box_id)
    text = strings.get_box_details(box)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.open_box(),
        parse_mode='HTML'
    )

    return State.MY_BOX


async def handle_courier_withdraw_request(update: Update, context: CallbackContext):
    text = strings.WITHDRAW_REQUEST_CREATED
    
    telegram_id = update.effective_chat.id
    
    await sync_to_async(bot_db.create_pickup_request)(
        address='уточнить при звонке',
        client_tg_id=telegram_id,
        request_type='withdraw'
    )

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )

    return State.MY_BOX


async def handle_send_qr(update: Update, context: CallbackContext):
    qr_path = path.join(BASE_DIR, f'{settings.STATIC}/qr_code.png')
    with open(qr_path, 'rb') as file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file
        )
    return State.MY_BOX


async def handle_put_items_to_box(update: Update, context: CallbackContext):
    text = strings.WRITE_DOWN_STORED_ITEMS

    menu_message = await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.open_box(),
        parse_mode='HTML'
    )

    context.user_data['menu_message_id'] = menu_message.message_id

    return State.PUT_ITEMS_INTO_BOX


async def validate_new_items(update: Update, context: CallbackContext):
    box_id = context.user_data['box_id']

    items: list[str] = update.message.text.split(',')

    parsed_items = [item.strip() for item in items if item]

    await sync_to_async(bot_db.add_new_items_to_box)(parsed_items, box_id)

    box = await sync_to_async(bot_db.get_box)(box_id)
    text = strings.get_box_details(box)

    await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data['menu_message_id'],
            text=text,
            parse_mode='HTML',
            reply_markup=keyboards.open_box()
    )

    return State.MY_BOX


async def handle_remove_items_from_box(update: Update, context: CallbackContext):
    text = strings.SELECT_RETRIEVED_ITEMS
    box_id = context.user_data['box_id']
    params = parse_callback_data_string(update.callback_query.data).params

    item_id = params.get('item_id')
    if item_id:
        await sync_to_async(bot_db.delete_item)(item_id)

    box = await sync_to_async(bot_db.get_box)(box_id)
    text = strings.get_box_details(box)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.remove_items_from_box(box),
        parse_mode='HTML'
    )
    return State.MY_BOX


async def handle_input_address(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.id
    user = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    if not user:
        await update.callback_query.edit_message_text(
            strings.PPD,
            reply_markup=keyboards.ppd_peyboard(),
            parse_mode='HTML'
        )
        return State.PERSONAL_DATA_AGREEMENT

    text = strings.ENTER_YOU_ADDRESS_FOR_COURIER

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )
    return State.INPUT_ADDRESS


async def handle_create_courier_delivery_request(update: Update, context: CallbackContext):
    address = context.user_data.get('address')
    telegram_id = update.effective_chat.id
    
    await sync_to_async(bot_db.create_pickup_request)(
        address=address,
        client_tg_id=telegram_id,
        request_type='deliver'
    )

    text = strings.DELIVERY_REQUEST_CREATED

    await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data['address_message_id'],
            text=text,
            reply_markup=keyboards.back_to_menu_keyboard(),
            parse_mode='HTML'
    )

    return State.CREATE_COURIER_DELIVERY_REQUEST


async def handle_select_warehouse(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.id
    user = await sync_to_async(bot_db.find_user_by_tg)(telegram_id)

    if not user:
        await update.callback_query.edit_message_text(
            strings.PPD,
            reply_markup=keyboards.ppd_peyboard(),
            parse_mode='HTML'
        )
        return State.PERSONAL_DATA_AGREEMENT

    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params

    page_number = params.get('page') or 1

    warehouses = await sync_to_async(bot_db.get_all_warehouses)()
    page: Page = Paginator(
        warehouses,
        per_page=settings.BUTTONS_PER_PAGE
    ).page(page_number)

    await update.callback_query.edit_message_text(
        strings.SELECT_WAREHOUSE,
        reply_markup=keyboards.warehouses_keyboard(page),
        parse_mode='HTML'
    )
    return State.SELECT_WAREHOUSE


async def handle_warehouse(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    params = parse_callback_data_string(update.callback_query.data).params
    warehouse_id = params.get('id')
    context.user_data['warehouse_id'] = warehouse_id
    warehouse = await sync_to_async(bot_db.get_warehouse)(warehouse_id)
    boxes = warehouse.get('boxes')
    text = strings.get_warehouse_details(warehouse)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.select_box(boxes),
        parse_mode='HTML'
    )

    return State.WAREHOUSE


async def handle_input_period(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    params = parse_callback_data_string(update.callback_query.data).params
    context.user_data['size_id'] = params.get('size_id')

    edit_message_text = strings.COMPLETE_ALL_STEPS_TO_MAKE_REQUEST
    new_message_text = strings.INPUT_RENT_PERIOD

    await update.callback_query.edit_message_text(
        edit_message_text,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=new_message_text,
            parse_mode='HTML'
    )

    return State.INPUT_RENT_PERIOD


async def validate_period(update: Update, context: CallbackContext):
    period = update.message.text
    if validators.period_is_valid(period):
        text = strings.PERIOD_IS_ACCEPTED_ENTER_PROMO.format(
            period=period
        )
        context.user_data['period'] = int(period)
        state = State.INPUT_PROMO
        keyboard = keyboards.promo()
    else:
        text = strings.PERIOD_IS_INCORRECT
        state = State.INPUT_RENT_PERIOD
        keyboard = None

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
    )

    return state


async def validate_promo(update: Update, context: CallbackContext):
    code = update.message.text
    promocode = await sync_to_async(bot_db.find_promocode)(code)

    if promocode.get('is_valid'):
        context.user_data['promocode'] = promocode
        size_id = context.user_data['size_id']
        warehouse_id = context.user_data['warehouse_id']

        warehouse = await sync_to_async(bot_db.get_warehouse)(warehouse_id)
        size = await sync_to_async(bot_db.get_box_size)(size_id)
        period = context.user_data['period']

        text = strings.get_box_rent_confirmation(
            warehouse,
            size,
            period,
            promocode
        )

        keyboard = keyboards.confirm_rent()
        state = State.CONFIRM_BOX_RENT
    else:
        state = State.INPUT_PROMO
        text = 'Извините, но такого промокода нет. Попробуйте еще раз'
        keyboard = None

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
    )

    return state


async def handle_confirm_box_rent(update: Update, context: CallbackContext):
    size_id = context.user_data['size_id']
    warehouse_id = context.user_data['warehouse_id']

    warehouse = await sync_to_async(bot_db.get_warehouse)(warehouse_id)
    size = await sync_to_async(bot_db.get_box_size)(size_id)
    promocode = context.user_data.get('promocode')
    period = context.user_data['period']

    text = strings.get_box_rent_confirmation(
        warehouse,
        size,
        period,
        promocode
    )

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.confirm_rent(),
        parse_mode='HTML'
    )

    return State.CONFIRM_BOX_RENT


async def handle_rent_box(update: Update, context: CallbackContext):
    telegram_id = update.effective_chat.id
    size_id = context.user_data['size_id']
    warehouse_id = context.user_data['warehouse_id']
    period = context.user_data['period']

    await sync_to_async(bot_db.add_box_to_user)(
        telegram_id,
        warehouse_id,
        size_id, period
    )

    text = strings.YOU_HAVE_RENTED_THE_BOX

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )

    return State.CONFIRM_BOX_RENT


async def handle_ppd_agreement(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        strings.PPD,
        reply_markup=keyboards.ppd_peyboard(),
        parse_mode='HTML'
    )
    return State.PERSONAL_DATA_AGREEMENT


async def validate_address(update: Update, context: CallbackContext):
    address = update.message.text

    if validators.name_is_valid(address):
        context.user_data['address'] = address
        text = strings.CONFIRM_YOUR_ADDRESS_AND_REQUEST.format(
            address=address
        )
        state = State.CREATE_COURIER_DELIVERY_REQUEST
        keyboard = keyboards.courier_delivery_request()

    else:
        text = strings.ADDRESS_IS_NOT_CORRECT.format(
            address=address
        )
        state = State.INPUT_ADDRESS
        keyboard = None

    address_message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
    )

    context.user_data['address_message_id'] = address_message.message_id

    return state


async def handle_input_name(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.INPUT_YOUR_FULLNAME_FOR_SIGNUP

    await update.callback_query.edit_message_text(
        strings.COMPLETE_ALL_STEPS_TO_SIGNUP,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML'
    )

    return State.INPUT_FULL_NAME


async def validate_full_name(update: Update, context: CallbackContext):
    name = update.message.text

    if validators.name_is_valid(name):
        text = strings.YOUR_NAME_IS_CORRECT.format(name=name)
        state = State.INPUT_PHONE
        context.user_data['full_name'] = name
    else:
        text = strings.YOUR_NAME_IS_INCORRECT.format(name=name)
        state = State.INPUT_FULL_NAME

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML'
    )

    return state


async def validate_phone(update: Update, context: CallbackContext):
    if validators.phone_is_valid(update.message.text):
        await update.message.reply_text(
            strings.YOUR_PHONE_IS_CORRECT,
        )
        context.user_data['phone'] = update.message.text
        return State.INPUT_EMAIL
    else:
        await update.message.reply_text(
            strings.YOUR_PHONE_IS_INCORRECT,
        )
        return State.INPUT_PHONE


async def validate_email(update: Update, context: CallbackContext):
    email = update.message.text

    if validators.email_is_valid(email):
        context.user_data['email'] = email
        text = strings.CONFIRM_SIGNUP.format(
            full_name=context.user_data['full_name'],
            phone=context.user_data['phone'],
            email=context.user_data['email']
        )

        state = State.SIGN_UP
        keyboard = keyboards.signup_keyboard()

    else:
        text = strings.YOUR_EMAIL_IS_INCORRECT.format(email=email)
        state = State.INPUT_EMAIL
        keyboard = None

    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
    )

    return state


async def handle_signup(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    text = strings.USER_REGISTRATION_COMPLETE.format(
        full_name=context.user_data['full_name'],
        phone=context.user_data['phone'],
        email=context.user_data['email']
    )

    client = {
        'full_name': context.user_data['full_name'],
        'phone': context.user_data['phone'],
        'email': context.user_data['email'],
        'telegram_id': update.callback_query.from_user.id
    }

    await bot_db.acreate_user(client, settings.CLIENT)

    await update.callback_query.edit_message_text(
        text,
        reply_markup=keyboards.back_to_menu_keyboard(),
        parse_mode='HTML'
    )
    return State.SIGN_UP


def get_handlers():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            State.MAIN_MENU: [
                CallbackQueryHandler(handle_tos, get_pattern(CallbackName.TERMS_OF_SERVICE)),
                CallbackQueryHandler(handle_my_account, get_pattern(CallbackName.MY_ACCOUNT)),
                CallbackQueryHandler(handle_order_storage, get_pattern(CallbackName.ORDER_STORAGE)),
                CallbackQueryHandler(handle_ppd_agreement, get_pattern(CallbackName.PERSONAL_DATA_AGREEMENT)),
                CallbackQueryHandler(handle_show_prices, get_pattern(CallbackName.SHOW_PRICES)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.MY_ACCOUNT: [
                CallbackQueryHandler(handle_my_orders, get_pattern(CallbackName.MY_ORDERS)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.TERMS_OF_SERVICE: [
                CallbackQueryHandler(handle_download_tos, get_pattern(CallbackName.DOWNLOAD_TOS)),
                CallbackQueryHandler(handle_faq, get_pattern(CallbackName.FAQ)),
                CallbackQueryHandler(handle_forbidden, get_pattern(CallbackName.FORBIDDEN_TO_STORE)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.ORDER_STORAGE: [
                CallbackQueryHandler(handle_show_prices, get_pattern(CallbackName.SHOW_PRICES)),
                CallbackQueryHandler(handle_input_address, get_pattern(CallbackName.COURIER_DELIVERY)),
                CallbackQueryHandler(handle_select_warehouse, get_pattern(CallbackName.SELECT_WAREHOUSE)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.SELECT_WAREHOUSE: [
                CallbackQueryHandler(handle_select_warehouse, get_pattern(CallbackName.SELECT_WAREHOUSE)),
                CallbackQueryHandler(handle_warehouse, get_pattern(CallbackName.WAREHOUSE)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.WAREHOUSE: [
                CallbackQueryHandler(handle_input_period, get_pattern(CallbackName.SELECT_BOX)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.INPUT_RENT_PERIOD: [
                MessageHandler(filters.TEXT, validate_period),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.INPUT_PROMO: [
                MessageHandler(filters.TEXT, validate_promo),
                CallbackQueryHandler(handle_confirm_box_rent, get_pattern(CallbackName.NO_PROMO)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.CONFIRM_BOX_RENT: [
                CallbackQueryHandler(handle_rent_box, get_pattern(CallbackName.CONFIRM_BOX_RENT)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.INPUT_ADDRESS: [
                MessageHandler(filters.ALL, validate_address),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.MY_ORDERS: [
                CallbackQueryHandler(handle_my_box, get_pattern(CallbackName.MY_BOX)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.MY_BOX: [
                CallbackQueryHandler(handle_put_items_to_box, get_pattern(CallbackName.PUT_NEW_ITEMS)),
                CallbackQueryHandler(handle_courier_withdraw_request, get_pattern(CallbackName.ORDER_DELIVERY)),
                CallbackQueryHandler(handle_my_orders, get_pattern(CallbackName.MY_ORDERS)),
                CallbackQueryHandler(handle_open_box, get_pattern(CallbackName.OPEN_BOX)),
                CallbackQueryHandler(handle_my_box, get_pattern(CallbackName.MY_BOX)),
                CallbackQueryHandler(handle_send_qr, get_pattern(CallbackName.OPEN_QR)),
                CallbackQueryHandler(handle_remove_items_from_box, get_pattern(CallbackName.REMOVE_ITEMS)),
                CallbackQueryHandler(handle_remove_items_from_box, get_pattern(CallbackName.REMOVE_ITEM)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.PUT_ITEMS_INTO_BOX: [
                MessageHandler(filters.TEXT, validate_new_items),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.PERSONAL_DATA_AGREEMENT: [
                CallbackQueryHandler(handle_input_name, get_pattern(CallbackName.INPUT_FULL_NAME)),
                CallbackQueryHandler(handle_download_ppd, get_pattern(CallbackName.DOWNLOAD_PPD)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.PERSONAL_DATA_DISAGREE)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
            State.INPUT_FULL_NAME: [
                MessageHandler(filters.ALL, validate_full_name),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.INPUT_PHONE: [
                MessageHandler(filters.ALL, validate_phone),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.INPUT_EMAIL: [
                MessageHandler(filters.ALL, validate_email),
                CallbackQueryHandler(handle_signup, get_pattern(CallbackName.SIGN_UP)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.SIGN_UP: [
                CallbackQueryHandler(handle_signup, get_pattern(CallbackName.SIGN_UP)),
                CallbackQueryHandler(handle_ppd_agreement, get_pattern(CallbackName.PERSONAL_DATA_AGREEMENT)),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
            ],
            State.CREATE_COURIER_DELIVERY_REQUEST: [
                CallbackQueryHandler(
                    handle_create_courier_delivery_request,
                    get_pattern(CallbackName.CREATE_COURIER_DELIVERY_REQUEST)
                ),
                CallbackQueryHandler(handle_back_menu, get_pattern(CallbackName.MAIN_MENU)),
                MessageHandler(filters.Regex(r'^(?!\/start).*'), unknown_cmd),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
