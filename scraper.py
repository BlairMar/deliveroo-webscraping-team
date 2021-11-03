#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

#%%

class Scraper:
    
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.get('https://deliveroo.co.uk')
        self.__accept_cookies()

    def __accept_cookies(self):
        time.sleep(0.1)   ##could have a shorter sleep time
        self.driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

    def __enter_address(self, address):
        # TODO
        pass
    
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

# %%
