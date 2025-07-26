# сюда функции для работы с бд джанго
import os
import django

os. environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_core.settings')
django.setup()

from bot_django_app.models import Client, StorageLocation


def get_user(id_user):
    return Client.objects.get(telegram_id=id_user)


def get_all_warehouses() -> list[dict]:
    return [warehouse.__dict__ for warehouse in StorageLocation.objects.all()]


def get_warehouse(pk: int) -> StorageLocation:
    return StorageLocation.objects.get(pk=pk)
