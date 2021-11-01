#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

#%%

class Scraper:
    
    def __init__(self, address) -> None:
        for place in address:
            self.driver = webdriver.Chrome()
            self.driver.get('https://deliveroo.co.uk')
            self.__accept_cookies()
            self.__enter_address(place)   ### Only works if 'mark location' button does not require the location pin to be moved

    def __accept_cookies(self):
        time.sleep(0.1)   ##could have a shorter sleep time
        self.driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

    def __enter_address(self, address):
        self.addressbar = self.driver.find_element(By.XPATH, '//*[@id="location-search"]')
        self.addressbar.send_keys(f'{address}')
        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/span/button').click()
        time.sleep(0.5)
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div/div[2]/div/span/button').click() 
        except:  ##if map location does not show 
            pass

#%%

buck = ['emirates stadium', 'buckingham palace']
example = Scraper(buck)
#%%

    def __acknowledge_voucher(self):
        # TODO
        pass
    
    def __sort_page(self, option):
        # TODO
        pass

    def __collect_restaurant_data(self, restaurant):
        # TODO
        pass
    
    def scrape(self):
        # TODO
        pass
