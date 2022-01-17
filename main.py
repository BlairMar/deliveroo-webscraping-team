
from scraper import Scraper
from database import set_up_database
from processing import image_process, process
from logger import set_up_logger
from config import set_up_config
from boto import Upload
import json

import os

def load_data(address, engine, conn):
    import pandas as pd
    from sqlalchemy import inspect
    
    ins = inspect(engine)
    if not ins.has_table(address):
        return []
        
    query = f'SELECT * FROM "{address}"'
    df = pd.read_sql(query, conn)
    return df.to_dict()

def set_up_dirs(output_loc):
    if os.path.isdir(f'{output_loc}/images'):
        pass
    else:
        os.makedirs(f'{output_loc}/images')

def main():
    address = 'SW1A 0AA'
    output_loc = f'data/{address}'
    set_up_config()
    set_up_dirs(output_loc)
    set_up_logger()
    engine = set_up_database()
    Upload.set_up_boto()
    
    with engine.connect() as conn:
        existing_data = load_data(address, engine, conn)
    
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

    try:
        image_process(output_loc)
    except:
        print('Unable to process and save images to s3..')


if __name__ == '__main__':
    main()

