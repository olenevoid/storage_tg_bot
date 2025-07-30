# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options

MAIN_MENU = (
    'Этот бот может использоваться для хранения всего, что можно хранить'
)

MY_ACCOUNT = (
        '<b>Личные данные пользователя</b>\n\n'
        '<b>Роль:</b> {role}\n'
        '<b>ФИО:</b> {full_name}\n'
        '<b>Телефон:</b> {phone}\n'
        '<b>E-mail:</b> {email}\n'        
        '<b>Зарегистрирован с:</b> {created_at}\n\n'
        '<b>{no_orders}</b>'
)

PPD = (
    'Пользоваться услугами нашего сервиса можно только после регистрации\n\n'
    'Для регистрации вам необходимо согласиться с обработкой ваших персональных данных\n\n'
    'Полный текст соглашения можете скачать по кнопке ниже\n\n'
    '<b>Вы согласны на обработку ваших персональных данных?</b>\n\n'
    'В случае отказа вы вернетесь в главное меню\n'
)

ORDER_STORAGE = (
    'Вы можете посмотреть расценки наших ячеек и выбрать удобный для вас способ доставки\n'
    'Учтите, что только зарегистрированные пользователи могут пользоваться нашими услугами'
)

TOS = (
    'Вот такие у нас условия обслуживания. По кнопке можете скачать полную версию'
)

FAQ = (
    '<b>В:</b> Могу ли я хранить всё, что угодно? \n'
    '<b>О:</b> Нет, не можете\n\n'
)

FORBIDDEN = (
    '<b>Запрещенные к хранению вещества:</b>\n'
    '1. Оружие\n'
    '2. Жидкости\n'
    '3.Любые живые животные и растения \n'
    
)

WITHDRAW_REQUEST_CREATED = (
    'Наш менеджер скоро с вами свяжется для уточнения деталей'
)


USER_REGISTRATION_COMPLETE = (
        'Пользователь зарегистрирован\n'
        'Имя: {full_name}\n'
        'Телефон: {phone}\n'
        'Имейл: {email}\n'
)

SELECT_WAREHOUSE = (
    'Выберите удобный вам склад из списка ниже:'
)

MY_BOX_DETAILS = (
        '<b>Размер ячейки:</b> {box_code}\n'
        '<b>Цена в месяц:</b> {box_price}\n'
        '<b>Адрес склада:</b> {address}\n'
        '<b>Арендована до:</b> {rented_until}\n'
        '<b>Предметы на хранении:</b>\n'
)

MY_BOXES = (
    'Ниже, в виде кнопок находятся ваши активные ячейки (если они у вас есть)\n'
    'Вы можете пользоваться ими свободно: забирать и возвращать вещи до конца аренды'
)


WRITE_DOWN_STORED_ITEMS = (
    'Введите через запятую названия предметов, которые положили в хранилище'
)


SELECT_RETRIEVED_ITEMS = (
    'Нажмите на предметы, которые хотите удалить'
)


ENTER_YOU_ADDRESS_FOR_COURIER = (
    'Введите свой адрес, чтобы мы могли определить ближайшего к вам курьера\n'
    'Или вернитесь в меню для отмены'
)


DELIVERY_REQUEST_CREATED = (
    'Заявка создана, ждите звонка\n'
    'Наш менеджер свяжется с вами для уточнения деталей:\n\n'
    '1. Примерное количество вещей и их габариты\n'
    '2. Удобное время для вывоза\n\n'
    'А пока можете перейти в меню условий обслуживания и убедиться, что вы не собираетесь передавать запрещенные для хранения вещи'
)


COMPLETE_ALL_STEPS_TO_MAKE_REQUEST = (
    'Пройдите все шаги, либо вернитесь в меню, если передумали'
)


INPUT_RENT_PERIOD = (
    'Введите количество месяцев для аренды (от 1 до 12)'
)


PERIOD_IS_ACCEPTED_ENTER_PROMO = (
    'Выбран период: {period}\n'
    'Теперь введите промокод, если он у вас есть'
)


PERIOD_IS_INCORRECT = (
    'Введен некорректный период.\n '
    'Вы можете указать от 1 до 12 месяцев'
)


YOU_HAVE_RENTED_THE_BOX = (
    'Ячейка успешно арендована!\n'
    'В личном кабинете вы сможете увидеть свои активные заказы\n'
    'Также, сможете там получить QR-код для открытия ячейки и составить список оставленных вещей\n'
)


CONFIRM_YOUR_ADDRESS_AND_REQUEST = (
    'Ваш адрес: {address}\n\n'
    'Создать заявку для вызова курьера?'
)


ADDRESS_IS_NOT_CORRECT = (
    'Вы ввели некорректный {address}, попробуйте еще раз'
)


INPUT_YOUR_FULLNAME_FOR_SIGNUP = (
    'Пожалуйста, введите ваши фамилию и имя (можно полностью ФИО)'
)


COMPLETE_ALL_STEPS_TO_SIGNUP = (
    'Пройдите все шаги регистрации, либо вернитесь в меню, если передумали'
)


YOUR_NAME_IS_CORRECT = (
    'Здравствуйте, {name}, теперь введите телефон'
)


YOUR_NAME_IS_INCORRECT = (
    'Вы ввели некорректное имя {name}, попробуйте еще раз'
)

YOUR_PHONE_IS_CORRECT = (
    'Отлично, теперь введите ваш email'
)


YOUR_PHONE_IS_INCORRECT = (
    'Некорректный формат номера. Введите номер в формате 7(8)1234567890'
)


CONFIRM_SIGNUP = (
    'Введенные данные корректны?\n'
    'Имя: {full_name}\n'
    'Телефон: {phone}\n'
    'Имейл: {email}\n'
)


YOUR_EMAIL_IS_INCORRECT = (
    'Вы ввели некорректный имейл {email}, попробуйте еще раз'
)


def get_box_details(box: dict):
    box_size = box.get('size')
    text = MY_BOX_DETAILS.format(
        box_code=box_size.get('code'),
        box_price=box_size.get('price'),
        address=box.get('address'),
        rented_until=box.get('rented_until')
    )

    for item in box.get('stored_items'):
        text += f'{item.get('name')}\n'

    text += (
        '\n<b>Список вещей составляется пользователем для собственных нужд\n'
        'Мы не несем отвестсвенность за его достоверность</b>'
    )

    return text


def get_user_details(user: dict):
    no_orders = f'{'' if user.get('boxes') else 'Нет активных заказов'}'

    text = MY_ACCOUNT.format(
        role=user.get('role'),
        full_name=user.get('full_name'),
        phone=user.get('phone'),
        email=user.get('email'),
        created_at=user.get('created_at'),
        no_orders=no_orders
    )

    return text


def get_sizes_with_details(sizes: dict):
    text = ''

    for size in sizes:
        text += (
            f'<b>Размер:</b> {size.get('code')}\n'
            f'<b>Объем:</b> {size.get('volume_m3')}\n'
            f'<b>Цена в месяц:</b> {size.get('price')} р.\n'
            '\n'
        )

    return text


def get_warehouse_details(warehouse: dict):
    boxes = warehouse.get('boxes')

    has_delivery_text = 'Нет'

    if warehouse.get('has_delivery'):
        has_delivery_text = 'Да'

    text = (
        f'Название: {warehouse.get('name')}\n'
        f'Адрес: {warehouse.get('address')}\n'
        f'Есть доставка: {has_delivery_text}\n'
    )

    for box in boxes:
        size = box.get('size')
        text += (
            f'Ячейка: {size.get('code')}\n'
            f'Цена: {size.get('price')}\n'
            f'Свободно: {box.get('available')}\n\n'
        )
    
    return text


def get_box_rent_confirmation(warehouse, size, period, promocode = None):
    price = float(size.get('price'))
    sum = int(price * period)
    
    sum_text = (
        f'Итоговая сумма: <b>{sum}</b>'
    )
    
    if promocode:
        discount_sum = sum - (sum / 100 * promocode.get('discount'))
        sum_text = f'Итоговая сумма: <s>{sum}</s> <b>{discount_sum}</b>'
    
    raw_text = (
        'Выбрана ячейка <b>{size_code}</b> объемом <b>{volume}</b> куб.м.\n'
        'По адресу: <b>"{warehouse_name}" {address}</b>\n'
        'Цена за месяц: <b>{price} руб.</b>\n'
        'Срок аренды (мес): <b>{period}</b>\n'
        '{sum_text}\n\n'
    )

    text = raw_text.format(
        size_code=size.get('code'),
        volume=size.get('volume_m3'),
        warehouse_name=warehouse.get('name'),
        address=warehouse.get('address'),
        price=price,
        period=period,
        sum_text=sum_text
    )

    if promocode:
        text += (
            f'Применен промокод: <b>{promocode.get('code')}</b>'
        )

    return text
