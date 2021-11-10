
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

import unittest
import sys

#%%

class Scraper:
    sorteddata ={}
    def __init__(self, address) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://deliveroo.co.uk')
        self.sort_options = {
            'Distance': 0,
            'Hygiene_ratings': 1,
            'Recommended': 2,
            'Time': 3,
            'Top_rated': 4
        }
        self.__accept_cookies()
        self.__enter_address(address)   ### Only works if 'mark location' button does not require the location pin to be moved
        self.__acknowledge_14_delivery()
        self.__sort_page()
        

    def __accept_cookies(self):
        time.sleep(1)   ##could have a shorter sleep time
        self.driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

    def __enter_address(self, address):
        self.addressbar = self.driver.find_element(By.XPATH, '//*[@id="location-search"]')
        self.addressbar.send_keys(f'{address}')
        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/span/button').click()
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div[2]/div/span/button').click() 
        except:  #if map location does not show 
            pass
        
    
    def __acknowledge_14_delivery(self):
        # TODO
        #find the "Ok button in 14 day delivery for new customers"
        time.sleep(1.5)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[8]/div/div/div/div/div/div[2]/span[2]/button').click()
            
        except:
            pass
             
        #driver.find_element(By.XPATH,'/html/body/div[8]/div/div/div/div/div/div[2]/span[2]/button').click()
    
    def __sort_page(self, option: str='Top_rated'):
        if option not in self.sort_options:
            raise ValueError("Option does not exist")
        try:
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/button').click()
            filter_list = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/div/ul')
            filter_list.find_elements(By.XPATH, './li/label/input')[self.sort_options[option]].click()
        except:
            pass
        
    def __collect_restaurants(self):
        res_menu = self.driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/ul')
        res_list = self.res_menu.find_elements(By.TAG_NAME,'li')
        urls = []
        for res in res_list:
            el = res.find_element(By.TAG_NAME,'a')
            res_name = el.text
            res_url = el.get_attribute('href')
            urls.append((res_name,res_url))
        return urls

    def getSummary(self):
        Summary_info = self.driver.find_elements(By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div/div[1]')
        rawdata = Summary_info[0].text.splitlines()
        Scraper.sorteddata = {
            'Name':rawdata[0],
             'Rating':None,
              'Tags': [],
               'Address':None,
               'Url':None
        }
        lower_bound, upper_bound = 0 ,0
        for item in rawdata:
            if '+ rating' in item:
                Scraper.sorteddata['Rating'] = item
                lower_bound = rawdata.index(item)+1
            elif 'View map' in item:
                upper_bound = rawdata.index(item)
                Scraper.sorteddata['Address'] = rawdata[upper_bound - 1]
                upper_bound -= 2 # setting upper bound to 2 elements before view map appears. 
        Scraper.sorteddata['Tags'] = [item for item in rawdata[lower_bound:upper_bound]]   
        self.getPicture()
        print(Scraper.sorteddata)
        return Scraper.sorteddata #defined as a global variable. 
    
    def getPicture(self):
        Image_info = self.driver.find_elements(By.XPATH,'//*[@class = "restaurant__image"]//*')
        txt = Image_info[1].get_attribute("style")
        src = txt.split('"') #Only need the url so the code splits string at ". 
        url = src[1]
        name = Scraper.sorteddata['Name']
        path = f'{name}.jpg' 
        image = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(image)
        #print(url)
        Scraper.sorteddata['Url'] = url
        return Scraper.sorteddata    

    def scrape(self):
        self.getSummary()

if __name__ == '__main__':
    
    scrapey = Scraper('E20AG')
    a = input('Do you want to continue?')
    #This input allows the user some time to click on the restaurant before continuing as 
    #that functionality is yet to be implemented.
    
    if a == ('y'):
        scrapey.scrape()

#%%

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.handle = open ('scraper.py')

    def test_address_input(self):
        address = 'buckingham palace'
        address_test = Scraper(address)
        address_test.__enter_address(address)
        self.assert #something
        ##test will not work until address is removed from __init__

    def scrape_data_test(self):
        address = 'buckingham palace'
        scraper_test = Scraper(address)
        scraper_test.scrape()
        self.assert #something

    
    def tearDown(self):
        self.handle.close()

if __name__ == '__main__':
    unittest.main(argv=[], verbosity=2, exit=False)
# %%
