import os
import django
from datetime import datetime, timedelta
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
            f"📦 Напоминание: срок хранения вещей в боксе #{box.id} закончился. "
            f"Пожалуйста, заберите их со склада или продлите аренду."
        )

        if not Notification.objects.filter(user=user, box=box, notification_type="monthly_reminder").exists():
            try:
                bot.send_message(chat_id=user.telegram_id, text=text)
                Notification.objects.create(
                    user=user,
                    box=box,
                    notification_type="monthly_reminder"
                )
                print(f"[INFO] Сообщение отправлено пользователю {user.full_name}")
            except Exception as e:
                print(f"[ERROR] Ошибка при отправке сообщения: {e}")


def warning_before_expiration_job():
    print("[SCHEDULER] Running 3-day warning job...")
    target_date = datetime.today().date() + timedelta(days=3)
    expiring_boxes = Box.objects.filter(end_date=target_date, is_active=True)

    for box in expiring_boxes:
        user = box.user
        text = (
            f"⏳ Напоминаем: срок хранения вашей коробки #{box.id} "
            f"заканчивается через 3 дня — {box.end_date}. "
            f"Продлите аренду или заберите вещи."
        )

        if not Notification.objects.filter(user=user, box=box, notification_type="expiration_warning").exists():
            try:
                bot.send_message(chat_id=user.telegram_id, text=text)
                Notification.objects.create(
                    user=user,
                    box=box,
                    notification_type="expiration_warning"
                )
                print(f"[INFO] Предупреждение за 3 дня отправлено пользователю {user.full_name}")
            except Exception as e:
                print(f"[ERROR] Ошибка при отправке предупреждения: {e}")


def overdue_storage_job():
    print("[SCHEDULER] Running overdue job...")
    today = datetime.today().date()
    overdue_boxes = Box.objects.filter(end_date__lt=today, is_active=True)

    for box in overdue_boxes:
        user = box.user
        text = (
            f"❗ Внимание: срок хранения коробки #{box.id} истёк {box.end_date}. "
            f"Хранение продолжается по повышенному тарифу. "
            f"Продлите аренду или заберите вещи."
        )

        if not Notification.objects.filter(user=user, box=box, notification_type="overdue_notice").exists():
            try:
                bot.send_message(chat_id=user.telegram_id, text=text)
                Notification.objects.create(
                    user=user,
                    box=box,
                    notification_type="overdue_notice"
                )
                print(f"[INFO] Просрочка отправлена пользователю {user.full_name}")
            except Exception as e:
                print(f"[ERROR] Ошибка при отправке уведомления о просрочке: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()

    
    scheduler.add_job(monthly_reminder_job, 'cron', day=1, hour=10)

    
    scheduler.add_job(warning_before_expiration_job, 'cron', hour=9)

    
    scheduler.add_job(overdue_storage_job, 'cron', hour=10, minute=30)

    scheduler.start()
    print("[SCHEDULER] Планировщик успешно запущен.")