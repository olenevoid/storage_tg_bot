from telegram.ext import ApplicationBuilder
from ptb.handlers import get_handlers
from ptb.settings import TG_BOT_TOKEN
from ptb.sheduler import start_scheduler


def main():
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(get_handlers())
    start_scheduler()
    app.run_polling()


if __name__ == "__main__":
    main()
