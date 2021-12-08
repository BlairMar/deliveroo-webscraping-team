#%%
import unittest

from selenium import webdriver
from scraper import Scraper
import time
import os
from selenium.webdriver.common.by import By

#%%

# Tests steps prior to running the core scraper.
class ScraperSetupTestCase(unittest.TestCase):

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)

    def test01_cookies_clicker(self):
        try:
            self.test1._accept_cookies()
        except:
            self.fail("_accept_cookies raised an error")
    
    def test02_address_input(self):
        self.test1._accept_cookies()
        self.test1._enter_address(self.address)
        time.sleep(2)
        title = self.test1.driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/div/div/div/div/h3')
        self.assertIn("Farnley and New Farnley", title.text)
    
    def test03_address_folders(self):
        directory_path =f'data/{self.address}/images'
        self.test1._address_folder()
        self.assertTrue(os.path.exists(directory_path))

    def test04_collect_restaurants(self):
        self.test1.driver.get('https://deliveroo.co.uk/restaurants/leeds/farnley-and-new-farnley?geohash=gcwcgwestutx&sort=rating')
        self.test1._accept_cookies()
        collect_url = self.test1._collect_restaurants(10)
        self.assertEqual(len(collect_url), 10)
    
    def tearDown(self):
        self.test1.driver.quit()
        # TODO: Delete 'data' folder

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
