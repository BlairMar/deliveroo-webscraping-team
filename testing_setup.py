#%%

import unittest
from scraper import Scraper

#%%

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.handle = open('scraper.py')
        self.address = 'LS12 5NJ'
        self.test1 = Scraper(self.address)

    def test_cookies_clicker(self):
        self.assertIsNone(self.test1._accept_cookies())

    # def test_address_input(self):
    #     self.test1._enter_address(self.address)

    #     # self.assertFalse(None)
    
    def tearDown(self):
        self.test1.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
