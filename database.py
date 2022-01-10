from sqlalchemy import create_engine

import os

class Config:
    PORT = 5432
    USER = 'postgres'
    PASSWORD = 'localpassword'
    NAME = 'DeliverooScrape'
    HOST = 'localhost'

def set_up_database():
    if 'RDS_HOSTNAME' not in os.environ:
        HOST = Config.HOST
        PORT = Config.PORT
        USER = Config.USER
        PASSWORD = Config.PASSWORD
        DBNAME = Config.NAME
    else:
        HOST = os.environ['RDS_HOSTNAME']
        PORT = os.environ['RDS_PORT']
        USER = os.environ['RDS_USERNAME']
        PASSWORD = os.environ['RDS_PASSWORD']
        DBNAME = os.environ['RDS_DB_NAME']
   
    
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    
    engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')
    print("Database connected!")
    return engine

