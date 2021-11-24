#%%

import unittest
from scraper import Scraper
import time

#%%

class ScraperTestCase(unittest.TestCase):

    restaurant_url = 'https://deliveroo.co.uk/restaurants/'

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)

    def test_cookies_clicker(self):
        self.assertIsNone(self.test1._accept_cookies())

    def test_address_input(self):
        self.test1._accept_cookies()
        self.test1._enter_address(self.address)
        self.test1.driver.get(self.restaurant_url)
        self.assertIn("delivery", self.test1.driver.title)
    
    def test_address_folders(self):
        directory_path =f'data/{self.address}/images'
        self.test1._address_folder()
        self.assertTrue(os.path.exists(directory_path))
        # self.assertFalse(None)

    # def test_scrape(self):
    #     self.test1.scrape()
    #     dictionary = self.test1.sorteddata
    # assertIn(some_key, some_dict)
    # assertIn(some_key, some_dict.keys())
    #def test_get_summary(self):

    def test_collect_restaurants(self):
        


        
    def tearDown(self):
        self.test1.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
