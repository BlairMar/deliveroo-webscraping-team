from sqlalchemy import create_engine
from config import config
from logger import log

def set_up_database():
    HOST = config['DB_HOST']
    PORT = config['DB_PORT']
    USER = config['DB_USER']
    PASSWORD = config['DB_PASSWORD']
    DBNAME = config['DB_NAME']
    
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    
    engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')
    log('info', "Database connected!", False)
    return engine

