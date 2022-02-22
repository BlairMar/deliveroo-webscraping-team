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
    config['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY_ID']
    config['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_ACCESS_KEY']
    config['REGION_NAME'] = os.environ['REGION_NAME']