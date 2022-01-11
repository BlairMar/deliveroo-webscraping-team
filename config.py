import os

config = {}
def set_up_config():
    config['DB_NAME'] = os.environ['DB_NAME']
    config['DB_USER'] = os.environ['DB_USER']
    config['DB_PASSWORD'] = os.environ['DB_PASSWORD']
    config['DB_PORT'] = os.environ['DB_PORT']
    config['DB_HOST'] = os.environ['DB_HOST']
    config['SENTRY_DSN'] = os.environ['SENTRY_DSN']
    config['SENTRY_ENVIRONMENT'] = os.environ['SENTRY_ENVIRONMENT']
    