# сюда функции для работы с бд джанго
import os
import django
from django.utils.timezone import localtime, timedelta
from django.db import transaction


os. environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from bot_django_app.models import (User,
                                   StorageLocation,
                                   Box,
                                   StoredItem,
                                   BoxSize,
                                   BoxAvailability,
                                   Role,
                                   PromoCode
                                   )


# TODO: Переделать все методы для async


def get_user(pk):
    return User.objects.get(pk=pk)


async def acreate_user(user: dict, role_name: str = 'Клиент'):
    new_user = User()
    new_user.full_name = user.get('full_name')
    new_user.telegram_id = user.get('telegram_id')
    new_user.phone = user.get('phone')
    new_user.email = user.get('email')
    new_user.consent_given = True
    new_user.role = await Role.objects.aget(name=role_name)

    await new_user.asave()


async def aphone_number_exists(phone: str):
    return await User.objects.filter(phone).aexists()


@transaction.atomic
def add_box_to_user(telegram_id, warehouse_id, size_id, period):
    user = User.objects.get(telegram_id=telegram_id)
    location = StorageLocation.objects.get(pk=warehouse_id)
    size = BoxSize.objects.get(pk=size_id)
    box_availability = BoxAvailability.objects.get(location=location)

    box = Box()
    box.user = user
    box.location = location
    box.size = size
    box.end_date = localtime() + timedelta(days=period*30)
    box.save()
    
    box_availability.occupied_boxes += 1
    box_availability.save()


def find_user_by_tg(telegram_id) -> dict | None:
    user_exists_in_db = user_exists(telegram_id)
    if user_exists_in_db:
        user = User.objects.get(telegram_id=telegram_id)
        return _serialize_user(user)
    return None


@transaction.atomic
def add_new_items_to_box(items: list, box_id):
    box = Box.objects.get(pk=box_id)
    
    for item in items:
        StoredItem.objects.create(
            box=box,
            name=item
        )


def delete_item(item_id):
    StoredItem.objects.get(pk=item_id).delete()


async def auser_exists(telegram_id) -> bool:
    user_exists = await User.objects.filter(telegram_id=telegram_id).aexists()
    return user_exists


def user_exists(telegram_id) -> bool:
    user_exists = User.objects.filter(telegram_id=telegram_id).exists()
    return user_exists


def get_all_warehouses() -> list[dict]:
    return [_serialize_warehouse(warehouse) for warehouse in StorageLocation.objects.all()]


def get_warehouse(pk: int) -> StorageLocation:
    location = StorageLocation.objects.get(pk=pk)    
    warehouse = _serialize_warehouse(location)

    return warehouse


def get_available_boxes_for_location(
        location: StorageLocation) -> list[BoxAvailability] | None:
    if BoxAvailability.objects.filter(location=location).exists():
        return BoxAvailability.objects.filter(location=location).all()
    return None


def get_box(box_id):
    box = Box.objects.get(pk=box_id)
    return _serialize_box(box)


def get_box_size(pk):
    box_size = BoxSize.objects.get(pk=pk)
    return _serialize_size(box_size)


def get_all_boxes_for_user(pk) -> list[dict]:
    user = get_user(pk=pk)
    if not Box.objects.filter(user=user).exists():
        return []

    boxes = []
    for box in Box.objects.filter(user=user).all():
        boxes.append(_serialize_box(box))
    return boxes


def get_all_sizes():
    serialized_sizes = []

    for size in BoxSize.objects.all():
        serialized_sizes.append(_serialize_size(size))

    return serialized_sizes


def _serialize_stored_items(box_id):
    items = StoredItem.objects.filter(box_id=box_id).all()

    return [_serialize_item(item) for item in items]


def _serialize_item(item: StoredItem):
    serialized_item = {
        'id': item.pk,
        'name': item.name,
        'quantity': item.quantity
    }
    return serialized_item


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
        'volume_m3': size.volume_m3,
        'price': size.price_per_month
    }

    return serialized_size


def _serialize_user(user: User):
    boxes = get_all_boxes_for_user(user.pk)

    serialized_user = {
        'id': user.pk,
        'tg_id': user.telegram_id,
        'role': user.role.name,
        'full_name': user.full_name,
        'phone': user.phone,
        'email': user.email,
        'consent_given': user.consent_given,
        'created_at': user.created_at.strftime('%d-%m-%Y'),
        'boxes': boxes
    }

    return serialized_user


def _serialize_available_boxes(box_availabilities: list[BoxAvailability]):
    available_boxes = []

    for box in box_availabilities:
        available_boxes.append(
            {
                'size': _serialize_size(box.size),
                'total': box.total_boxes,
                'occupied': box.occupied_boxes,
                'available': box.available_boxes
            }
        )

    return available_boxes


def _serialize_warehouse(location: StorageLocation) -> dict:
    warehouse_boxes = get_available_boxes_for_location(location)

    warehouse = {
        'id': location.pk,
        'name': location.name,
        'address': location.address,
        'has_delivery': location.has_delivery,
        'is_active': location.is_active,
        'boxes': _serialize_available_boxes(warehouse_boxes)
    }

    return warehouse


def _serialize_promocode(promocode: PromoCode) -> dict:
    serialized_promocode = {
        'id': promocode.pk,
        'code': promocode.code,
        'discount': promocode.discount_percent,
        'valid_from': promocode.valid_from.strftime('%d-%m-%Y'),
        'valid_until': promocode.valid_until.strftime('%d-%m-%Y'),
        'is_active': promocode.is_active,
        'is_valid': promocode.is_valid()
    }
    
    return serialized_promocode
