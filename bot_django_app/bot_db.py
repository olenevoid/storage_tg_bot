# сюда функции для работы с бд джанго
import os
import django

os. environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from bot_django_app.models import Client, StorageLocation, Box, StoredItem, BoxSize


# TODO: Переделать все методы для async


def get_client(pk):
    return Client.objects.get(pk=pk)


async def user_exists(id_user) -> bool:
    user_exists = await Client.objects.filter(telegram_id=id_user).aexists()
    return user_exists


def get_all_warehouses() -> list[dict]:
    return [warehouse.__dict__ for warehouse in StorageLocation.objects.all()]


def get_warehouse(pk: int) -> StorageLocation:
    return StorageLocation.objects.get(pk=pk)


def get_box(box_id):
    box = Box.objects.get(pk=box_id)
    return _serialize_box(box)


def get_all_boxes_for_user(client_tg) -> dict:
    client = get_user(client_tg)
    boxes = []
    for box in Box.objects.filter(client=client).all():
        boxes.append(_serialize_box(box))
    return boxes


def _serialize_stored_items(box_id):
    items = StoredItem.objects.filter(box_id=box_id).all()

    return [f'{item.name} x {item.quantity} шт.' for item in items]


def _serialize_box(box: Box):
    rented_until = box.extended_until or box.end_date

    serialized_box = {
            'id': box.pk,
            'size': _serialize_size(box.size),
            'location': box.location.name,
            'address': box.location.address,
            'description': box.description,
            'rented_until': rented_until.strftime('%d-%m-%Y'),
            'stored_items': _serialize_stored_items(box.pk)
    }

    return serialized_box


def _serialize_size(size: BoxSize):
    serialized_size = {
        'id': size.pk,
        'code': size.code,
        'name': size.name,
        'price': size.price_per_month
    }

    return serialized_size
