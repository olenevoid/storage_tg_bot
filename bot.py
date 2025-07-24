from telegram.ext import ApplicationBuilder
from ptb.handlers import get_handlers
from environs import Env
env = Env()
env.read_env()
        
    
def main():
    app = ApplicationBuilder().token(env.str("TG_BOT_TOKEN")).build()
    
    for handler in get_handlers():
        app.add_handler(handler)
        
    app.run_polling()
    

if __name__ == "__main__":
    main()
    