from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from environs import Env
env = Env()
env.read_env()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(env.str("TG_TOKEN")).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()