from scraper import Scraper
from database import set_up_database
from data_processing import process

def load_data(address, conn):
    import pandas as pd
    
    query = f'SELECT * FROM {address}'
    df = pd.read_sql(query, conn)
    return df.to_dict()

def main():    
    address = 'LS12 5NJ'
    
    engine = set_up_database()
    with engine.connect() as conn:
        existing_data = load_data(address, conn)
    
    scraper = Scraper(address, existing_data)
    data = scraper.scrape(5)
    try:
        df = process(data)
        with engine.connect() as conn:
            df.to_sql(f'{address}', conn, if_exists='replace')
    except:
        print('Unable to process and save data to db...')
   
if __name__ == '__main__':
    main()
