
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

class Scraper:
    """
    This class is used to scrape data from Deliveroo.
    
    Attributes:
    Address (string): The postcode of the area of restaurants to be scraped. 
    """
    sorteddata ={}
    def __init__(self, address: str) -> None:
        """
        See help(Scraper) for accurate signature.
        """
        self.driver = webdriver.Chrome()
        self.driver.get('https://deliveroo.co.uk')
        self.sort_options = {
            'Distance': 0,
            'Hygiene_ratings': 1,
            'Recommended': 2,
            'Time': 3,
            'Top_rated': 4
        }
        self.address = address
        print(self.driver.find_element(By.XPATH,'//*'))

    def _accept_cookies(self):
        time.sleep(1.5)   ##self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
        return

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
        
    def __collect_restaurants(self, limit: int=None):
        res_menu = self.driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/ul')
        res_list = res_menu.find_elements(By.TAG_NAME,'li')
        urls = []
        for res in res_list:
            try:
                if limit is not None and len(urls) >= limit:
                    break
                el = res.find_element(By.TAG_NAME,'a')
                res_name = el.text
                res_url = el.get_attribute('href')
                urls.append((res_name,res_url))
            except:
                pass
        return urls

    def __get_summary(self):
        try:
            Summary_info = self.driver.find_elements(By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div/div[1]')
            rawdata = Summary_info[0].text.splitlines()
        except:
            Summary_info = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div/div/div[2]')
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
        self.__get_picture()
        print(Scraper.sorteddata)
        return Scraper.sorteddata #defined as a global variable. 
    
    def __get_picture(self):
        try:
            Image_info = self.driver.find_elements(By.XPATH,'//*[@class = "restaurant__image"]//*')
            txt = Image_info[1].get_attribute("style")
        except:
            Image_info = self.driver.find_elements(By.XPATH,'//*[@class = "MenuHeader-cf659db292cfad50"]/*')
            txt = Image_info[0].get_attribute("style")
        src = txt.split('"') #Only need the url so the code splits string at ". 
        url = src[1]
        name = Scraper.sorteddata['Name']
        path = f'{name}.jpg' 
        image = requests.get(url).content
        try:
            with open(path, 'wb') as handler:
                handler.write(image)
        except:
            print('Unable to save restaurant image')
        Scraper.sorteddata['Url'] = url
        return Scraper.sorteddata    

    def scrape(self):
        """
        This function calls private members of the scrape class and returns data on restaurants on deliveroo.
        
        Returns:
        Dictionary of scraped data and jpgs of the restaurants.
        """
        self.__accept_cookies()
        self.__enter_address(self.address)
        self.__acknowledge_14_delivery()
        self.__sort_page()
        time.sleep(5)
        urls = self._collect_restaurants(10)
        for (name, url) in urls:
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(5)
            self.__get_summary()
# %%

help(Scraper)
# %%
