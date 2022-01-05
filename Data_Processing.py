#%%

from numpy import NaN
from sqlalchemy import create_engine
import pandas as pd

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'ElSiraajy92!'
DATABASE = 'DeliverooScrape'
PORT = 5432

address = 'SW1A 0AA'

df = pd.read_json(f'data/{address}/data.json')
df.columns = ['tags', 'name', 'image_path','uuid', 'url', 'rating']

def list_to_string(my_list):
    if not my_list:
        return None
    else:
        return my_list[0]

#pd.options.mode.chained_assignment = None

def list_of_items_by_word(string_1, string_2='ignore', string_3='ignore'):
    
    lis = [list_to_string([strings for strings in tags if 
    string_1 in strings or string_2 in strings or string_3 in strings]) 
    for tags in df['tags']]
    remove_from_tags_by_list(lis)    
    return lis    

def remove_from_tags_by_list(list_1):
    [tags.remove(val) for val in list_1 for tags in df['tags'] if val in tags]

def remove_from_tags_by_string(string_1, string_2='ignore', string_3='ignore', string_4='ignore'):
    [tags.remove(val) for tags in df['tags']
    for val in tags if string_1 in val or string_2 in val or string_3 in val or string_4 in val]

# for count, string in enumerate(df['rating']):
#     string = str(string)
#     if any(chr.isdigit() for chr in string) == True and '.' in string:
#         pass
#     else:
#         print(df['rating'][count])

rating = list_of_items_by_word('Excellent', 'Very good', 'Good')
remove_from_tags_by_string('(',')')
missing_rating = pd.isnull(df["rating"])
df["rating"][missing_rating] = rating
# df["rating"] = df["rating"].str.replace('Excellent' or 'Very good' or 'Good','')

min_spend = list_of_items_by_word('minimum')
df['minimum_spend'] = min_spend
df['minimum_spend'] = df['minimum_spend'].str.replace('£', '')

closing = list_of_items_by_word('Closes at', 'Open until')
df['closing_time'] = closing

opening = list_of_items_by_word('Opens at')
df['opening_time'] = opening

distance = list_of_items_by_word("miles away", 'mile away')
df['distance'] = distance

delivery_charge = list_of_items_by_word('delivery')
df['delivery_charge'] = delivery_charge
df['delivery_charge'] = df['delivery_charge'].str.replace('£', '')
df['delivery_charge'] = df['delivery_charge'].str.replace('delivery', '')
df['delivery_charge'] = df['delivery_charge'].str.replace('Free', '0')

rawtagslist = []

for lis in df['tags']:
    for string in lis:
        if string in rawtagslist:
            pass
        elif 'Info' in string or 'View map' in string or 'Delivered by' in string or 'order' in string or 'Editions' in string:
            pass        
        elif ' ' in string:
            if any(chr.isdigit() for chr in string) == True and 'min' not in string:
                pass
            else:
                rawtagslist.append(string)                
        else:
            rawtagslist.append(string)

for tags in df['tags']:
    for string in tags:
        if string in rawtagslist:
            pass
        else: 
            tags.remove(string)

remove_from_tags_by_string('View map', 'Editions','Delivered by', 'updates')

delivery_time = list_of_items_by_word('-', 'min')
df['delivery_time'] = delivery_time

engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
df.to_sql(f'{address}',engine, if_exists='replace')

# %%
