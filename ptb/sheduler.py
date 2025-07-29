import os
import django
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from ptb.settings import TG_BOT_TOKEN


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot_core.settings")
django.setup()


from bot_django_app.models import Box, Notification


bot = Bot(token=TG_BOT_TOKEN)


def monthly_reminder_job():
    print("[SCHEDULER] Running monthly reminder job...")
    today = datetime.today().date()
    expired_boxes = Box.objects.filter(end_date__lt=today, is_active=True)

    for box in expired_boxes:
        user = box.user
        text = (
            f"Напоминание: срок хранения вещей в боксе #{box.id} закончился!!! "
            f"Пожалуйста, заберите их со склада или продлите аренду."
        )

        try:
            bot.send_message(chat_id=user.telegram_id, text=text)
            Notification.objects.create(
                user=user,
                box=box,
                notification_type="monthly_reminder"
            )
            print(f"Сообщение отправлено пользователю {user.full_name}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(monthly_reminder_job, 'cron', day=1, hour=10)  
    scheduler.start()
    print("[SCHEDULER] Запущен планировщик.")
