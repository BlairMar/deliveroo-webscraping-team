#%%

import unittest
from scraper import Scraper

#%%

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.handle = open ('scraper.py')
        self.address = 'buckingham palace'
        self.test1 = Scraper(self.address)

    def test_address_input(self):
        self.test1.__enter_address()
        self.assertEqual(None) #something
        ##test will not work until address is removed from __init__

    def scrape_data_test(self):
        self.test1.scrape()
        self.assert #something

    
    def tearDown(self):
        self.handle.close()

if __name__ == '__main__':
    unittest.main(argv=[], verbosity=2, exit=False)

