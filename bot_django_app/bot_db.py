# сюда функции для работы с бд джанго
from bot_django_app.models import Client

def get_user(id_user):
    return Client.objects.get(telegram_id=id_user)