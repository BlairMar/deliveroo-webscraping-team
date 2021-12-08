#%%

from typing import Collection
import unittest

from selenium import webdriver
from scraper import Scraper
import time
import os
from selenium.webdriver.common.by import By

#%%
# test1 = Scraper('LS12 5NJ')
# test1._accept_cookies()
# test1._enter_address('LS12 5NJ')
# test1._acknowledge_popups()
# test1._sort_page()
# test1._collect_restaurants()
# for i, url in enumerate(test1._collect_restaurants()):
#     if 



#%%


class ScraperSetupTestCase(unittest.TestCase):

    # restaurant_url = 'https://deliveroo.co.uk/restaurants/'

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)
        # self.driver = webdriver.Chrome()
        # self.driver.get('https://deliveroo.co.uk')
    

    def test01_cookies_clicker(self):
        try:
            self.test1._accept_cookies()
        except:
            self.fail("_accept_cookies raised an error")
    
    def test02_address_input(self):
        self.test1._accept_cookies()
        self.test1._enter_address(self.address)
        time.sleep(2)
        # self.test1.driver.get(self.restaurant_url)
        title = self.test1.driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/div/div/div/div/h3')
        self.assertIn("Farnley and New Farnley", title.text)
    
    def test03_address_folders(self):
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

    def test04_collect_restaurants(self):
        self.test1.driver.get('https://deliveroo.co.uk/restaurants/leeds/farnley-and-new-farnley?geohash=gcwcgwestutx&sort=rating')
        self.test1._accept_cookies()
        collect_url = self.test1._collect_restaurants(10)
        self.assertEqual(len(collect_url), 10)
    
        
        # self.assertEqual(collect_url, self.urls)
    #     # print("This is a test on the sucessful collection")

    def test05_get_summary(self):
    #TODO: check get summary does not raise an error and out of dictionary isnt empty.
        self.test1.driver.get('https://deliveroo.co.uk/menu/leeds/central-beeston/nisa-beeston?day=today&geohash=gcwcgwestuxg&time=ASAP')
        self.test1._accept_cookies()
        get_summary_data = self.test1._get_summary()
        if self.assertEqual(len(get_summary_data), 0):
            print("Empty")
        else:
            print("All good")    
        #if self.assertFalse(len(get_summary_data),0):
            #raise ValueError
        #pass

        
    def tearDown(self):
        self.test1.driver.quit()
        # TODO: Delete 'data' folder

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
