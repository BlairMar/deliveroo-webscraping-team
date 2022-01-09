from scraper import Scraper
from database import set_up_database
from data_processing import process

def main():    
    engine = set_up_database()
    address = 'LS12 5NJ'
    scraper = Scraper(address)
    data = scraper.scrape(5)
    try:
        df = process(data)
        df.to_sql(f'{address}', engine, if_exists='replace')
    except:
        print('Unable to process and save data to db...')
   
if __name__ == '__main__':
    main()
