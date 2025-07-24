# сюда функции для работы с бд джанго
from bot.models import Client

def get_user(id_user):
    user = Client.objects.get(telegram_id=id_user)
    return user