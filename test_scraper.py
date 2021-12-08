#%%

import unittest

from selenium import webdriver
from scraper import Scraper
import time
import os
from selenium.webdriver.common.by import By

# %%
# Tests for the core scraper functionality
class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)
    
    def test01_get_summary(self):
        #check get summary does not raise an error and out of dictionary isnt empty.
        self.test1._address_folder()
        self.test1.driver.get('https://deliveroo.co.uk/menu/leeds/central-beeston/nisa-beeston?day=today&geohash=gcwcgwestuxg&time=ASAP')
        self.test1._accept_cookies()
        get_summary_data = self.test1._get_summary()
        self.assertNotEqual(len(get_summary_data), 0)
        try: 
            self.test1._get_summary()
        except:
            self.fail("_get_summary raise an error")
        #TODO: Data Validation
        
    def tearDown(self):
        self.test1.driver.quit()
        # TODO: Delete 'data' folder

# unittest.main(argv=[''], verbosity=2, exit=False)
# %%
