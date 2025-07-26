from telegram.ext import ApplicationBuilder
from ptb.handlers import get_handlers
from environs import Env
env = Env()
env.read_env()
        
    
def main():
    app = ApplicationBuilder().token(env.str("TG_BOT_TOKEN")).build()
    
    app.add_handler(get_handlers())
        
    app.run_polling()
    

if __name__ == "__main__":
    main()
    