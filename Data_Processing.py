#%%

from numpy import NaN
from sqlalchemy import create_engine
import pandas as pd

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'FzA2609042102Ege'
DATABASE = 'DeliverooScrape'
PORT = 5432

address = 'BS1 4ER'

df = pd.read_json(f'data/{address}/data.json')
df.columns = ['tags', 'name', 'image_path','uuid', 'url', 'rating']


def my_func(my_list):
    if not my_list:
        return None
    else:
        return my_list[0]

pd.options.mode.chained_assignment = None

rating = [my_func([strings for strings in tags if 'Excellent' in strings or 'Very good' in strings]) for tags in df['tags']]
# [df["rating"].fillna(rat, inplace=True) 
# #   for rat in rating for tags in df['tags']if rat in tags]
[tags.remove(rat) for rat in rating for tags in df['tags'] if rat in tags]
missing_rating = pd.isnull(df["rating"])
df["rating"][missing_rating] = rating
[tags.remove(rate) for tags in df['tags'] for rate in tags if ')' in rate and '(' in rate]


min_spend = [my_func([strings for strings in tags if 'minimum' in strings]) for tags in df['tags']]
[tags.remove(spend) for spend in min_spend for tags in df['tags'] if spend in tags]
df['minimum_spend'] = min_spend
df['minimum_spend'] = df['minimum_spend'].str.replace('£', '')

closing = [my_func([strings for strings in tags if 'Closes at' in strings or 'Open until' in strings]) for tags in df['tags']]
[tags.remove(time) for time in closing for tags in df['tags'] if time in tags]
df['closing_time'] = closing

opening = [my_func([strings for strings in tags if 'Opens at' in strings]) for tags in df['tags']]
[tags.remove(opens) for opens in opening for tags in df['tags'] if opens in tags]
df['opening_time'] = opening

distance = [my_func([strings for strings in tags if 'miles away' in strings or 'mile away' in strings]) for tags in df['tags']]
[tags.remove(dist) for dist in distance for tags in df['tags'] if dist in tags]
df['distance'] = distance

delivery_charge = [my_func([strings for strings in tags if 'delivery' in strings]) for tags in df['tags']]
[tags.remove(charge) for charge in delivery_charge for tags in df['tags'] if charge in tags]
df['delivery_charge'] = delivery_charge

delivery_time = [my_func([strings for strings in tags if '-' in strings or 'min' in strings]) for tags in df['tags']]
[tags.remove(long) for long in delivery_time for tags in df['tags'] if long in tags]
df['delivery_time'] = delivery_time


rawtagslist = []

for lis in df['tags']:
    for string in lis:
        if string in rawtagslist:
            pass
        elif 'Info' in string or 'View map' in string or 'Delivered by' in string or 'order' in string or 'Editions' in string:
            pass        
        elif ' ' in string:
            if any(chr.isdigit() for chr in string) == True:
                pass
            else:
                rawtagslist.append(string)                
        else:
            rawtagslist.append(string)

print(rawtagslist)

for tags in df['tags']:
    for string in tags:
        if string in rawtagslist:
            pass
        else: 
            tags.remove(string)

[tags.remove('View map') for tags in df['tags'] if 'View map' in tags] 
 
[tags.remove(val) for tags in df['tags'] for val in tags if 'Editions' in val or 'delivered by' in val] 


engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
df.to_sql(f'{address}',engine, if_exists='replace')

# %%
