#%%

import unittest
from scraper import Scraper

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
        self.test1._enter_address(self.address)
        self.test1.driver.get(self.restaurant_url)
        self.assertIn("restaurants", self.test1.driver.title)

        # self.assertFalse(None)

    # def test_scrape(self):
    #     self.test1.scrape()
    #     dictionary = self.test1.sorteddata
    #     self.assertIsNotNone(dictionary)
    
    def tearDown(self):
        self.test1.driver.quit()

unittest.main(argv=[''], verbosity=2, exit=False)


# %%
