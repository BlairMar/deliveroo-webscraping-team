from datetime import datetime
from config import config
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

import sentry_sdk

def set_up_logger():
    sentry_sdk.init(
        dsn=config['SENTRY_DSN'],
        environment=config['SENTRY_ENVIRONMENT'],
        integrations=[SqlalchemyIntegration()]
    )

def log(level, message, sentry=True):
    lvl = level
    if level not in ['info', 'warn', 'error', 'fatal']:
        lvl = 'debug'
    if sentry:
        sentry_sdk.capture_message(lvl, message)
    print(f'{datetime.now()} - {lvl.upper()}: {message}')