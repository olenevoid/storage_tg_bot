from bot_settings import TG_TOKEN, READ_TIMEOUT, WRITE_TIMEOUT, POLL_INTERVAL
from handlers import handle_message, start_command, error, handle_buttons
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler


def create_bot_app():

    app = Application.builder().token(TG_TOKEN).read_timeout(READ_TIMEOUT).write_timeout(WRITE_TIMEOUT).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(handle_buttons))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    return app


def main():
    bot = create_bot_app()

    bot.run_polling(poll_interval=POLL_INTERVAL)


if __name__ == '__main__':
    main()
