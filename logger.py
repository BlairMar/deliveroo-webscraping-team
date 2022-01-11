from datetime import datetime
from config import config
import sentry_sdk

def set_up_logger():
    sentry_sdk.init(
        dsn=config['SENTRY_DSN'],
        environment=config['SENTRY_ENVIRONMENT']
    )

def log(level, message):
    lvl = level
    if level not in ['info', 'warn', 'error', 'fatal']:
        lvl = 'debug'
    sentry_sdk.capture_message(lvl, message)
    print(f'{datetime.now()} - {lvl.upper()}: {message}')