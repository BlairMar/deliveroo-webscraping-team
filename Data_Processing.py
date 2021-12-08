#%%

from sqlalchemy import create_engine
import pandas as pd

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'password'
DATABASE = 'DeliverooScrape'
PORT = 5432

df = pd.read_json('data/LS12 5NJ/data.json')
df.columns = ['tags', 'name', 'image_path','uuid', 'url']
df['tags'] = df['tags'].str.join(', ')
df['tags'] = df['tags'].str.replace('£', '')

engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
df.to_sql('deliveroo_data',engine, if_exists='replace')
# %%
