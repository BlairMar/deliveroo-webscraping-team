from datetime import datetime
import sentry_sdk

def set_up_logger(dsn, env='local'):
    sentry_sdk.init(
        dsn,
        environment=env
    )

def log(level, message):
    lvl = level
    if level not in ['info', 'warn', 'error', 'fatal']:
        lvl = 'debug'
    sentry_sdk.capture_message(lvl, message)
    print(f'{datetime.now()} - {lvl.upper()}: {message}')