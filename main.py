from scraper import Scraper
from database import set_up_database
from data_processing import process
from logger import set_up_logger

import os

def load_data(address, conn):
    import pandas as pd
    
    query = f'SELECT * FROM {address}'
    df = pd.read_sql(query, conn)
    return df.to_dict()

def set_up_dirs(output_loc):
    if os.path.isdir(f'{output_loc}/images'):
        pass
    else:
        os.makedirs(f'{output_loc}/images')

def main():
    address = 'LS12 5NJ'
    output_loc = f'data/{address}'
    set_up_dirs(output_loc)
    set_up_logger("https://d2744aa667304febbb8766ca55f650f8@o1086610.ingest.sentry.io/6098931")
    engine = set_up_database()
    
    with engine.connect() as conn:
        existing_data = load_data(address, conn)
    
    scraper = Scraper(address, existing_data, output_loc)
    data = scraper.scrape(5)
    try:
        df = process(data)
        with engine.connect() as conn:
            df.to_sql(f'{address}', conn, if_exists='replace')
    except:
        print('Unable to process and save data to db...')
        print('Saving to json instead...')
        with open(f'{output_loc}/data.json', 'w') as outfile:
            json.dump(data, outfile,indent=2)
   
if __name__ == '__main__':
    main()
