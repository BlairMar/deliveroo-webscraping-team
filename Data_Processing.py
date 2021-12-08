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

address = 'SW1A 0AA'

df = pd.read_json(f'data/{address}/data.json')
df.columns = ['tags', 'name', 'image_path','uuid', 'url', 'rating']
# df['tags'] = df['tags'].str.replace('£', '')
# minimum_charge = []
# for tags in df['tags']:
#     for strings in tags:
#         if 'minimum' in strings:
#             strings.replace('£', '')
#             minimum_charge.append(strings)
#             # minimum_charge = df.loc[strings]
#             # print(minimum_charge)
# print(minimum_charge)

# min_charge = [[strings for strings in tags if 'minimum' in strings] for tags in df['tags']]
# df['minimum_charge'] = min_charge

def my_func(my_list):
    if not my_list:
        return None
    else:
        return my_list[0]

min_charge = [my_func([strings for strings in tags if 'minimum' in strings]) for tags in df['tags']]
df['minimum_charge'] = min_charge
df['minimum_charge'] = df['minimum_charge'].str.replace('£', '')

closing = [my_func([strings for strings in tags if 'Closes at' in strings or 'Open until' in strings]) for tags in df['tags']]
df['closing_time'] = closing



engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
df.to_sql(f'{address}',engine, if_exists='replace')
# %%
