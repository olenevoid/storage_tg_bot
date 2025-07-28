from environs import env
from enum import Enum


env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
BUTTONS_PER_PAGE = 4


# Значения должны совпадать с ролями в БД
class RoleName(Enum):
    Administrator = 'Администратор'
    Courier = 'Курьер'
    Client = 'Клиент'