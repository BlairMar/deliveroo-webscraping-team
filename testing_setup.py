#%%

from typing import Collection
import unittest

from selenium import webdriver
from scraper import Scraper
import time
import os

#%%
test1 = Scraper('LS12 5NJ')
test1._accept_cookies()
test1._enter_address('LS12 5NJ')
test1._acknowledge_popups()
test1._sort_page()
test1._collect_restaurants()
for i, url in enumerate(test1._collect_restaurants()):
    if 



#%%


class ScraperTestCase(unittest.TestCase):

    # restaurant_url = 'https://deliveroo.co.uk/restaurants/'

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)
        # self.driver = webdriver.Chrome()
        # self.driver.get('https://deliveroo.co.uk')
    

    def test_cookies_clicker(self):
        self.assertIsNone(self.test1._accept_cookies())

    def test_address_input(self):
        self.test1._accept_cookies()
        self.test1._enter_address(self.address)
        # self.test1.driver.get(self.restaurant_url)
        self.assertIn("Deliveroo", self.test1.driver.title)
    
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
        self.test1.scrape()
        collect_url = self.test1._collect_restaurants('https://deliveroo.co.uk/menu/')
        print(collect_url)
        # self.assertEqual(collect_url, self.urls)
        # print("This is a test on the sucessful collection")



        
    def tearDown(self):
        self.test1.driver.quit()
        #self.driver.close()

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
