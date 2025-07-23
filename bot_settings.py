from environs import env

env.read_env()

TG_TOKEN = env('TG_TOKEN')
READ_TIMEOUT = env.int('READ_TIMEOUT', 60)
WRITE_TIMEOUT = env.int('WRITE_TIMEOUT', 60)
POLL_INTERVAL = env.int('POLL_INTERVAL', 3)