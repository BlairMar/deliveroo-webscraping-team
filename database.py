from sqlalchemy import create_engine

import os

class Config:
    PORT = 5432
    USER = 'scraper'
    PASSWORD = 'p#qV1v^YhR*j'
    NAME = 'postgresdb'
    HOST = 'deliveroo_db'

def set_up_database():
    HOST = os.environ['RDS_HOSTNAME']
    PORT = os.environ['RDS_PORT']
    USER = os.environ['RDS_USERNAME']
    PASSWORD = os.environ['RDS_PASSWORD']
    DBNAME = os.environ['RDS_DB_NAME']
    if HOST == '':
        HOST = Config.HOST
        PORT = Config.PORT
        USER = Config.USER
        PASSWORD = Config.PASSWORD
        DBNAME = Config.NAME
    
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    
    engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')
    print("Database connected!")
    return engine

