
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

#%%

class Scraper:
  
    data = []
    def __init__(self, address: str) -> None:
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
        
    
    def __acknowledge_14_delivery(self):
        # TODO
        #find the "Ok button in 14 day delivery for new customers"
        time.sleep(1)
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
        res_list = res_menu.find_elements(By.TAG_NAME,'li')
        urls = []
        for res in res_list:
            try:
                el = res.find_element(By.TAG_NAME,'a')
                res_name = el.text
                res_url = el.get_attribute('href')
                urls.append((res_name,res_url))
            except:
                pass
        return urls

    def __get_summary(self):
        Summary_info = self.driver.find_elements(By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div/div[1]')

        for info in Summary_info: #Looping over list of summary information about the restaraunt.     
            text = info.text
            Scraper.data = text.splitlines()
            #splits the string at new lines and stores as a list. 
            #at some point, we need to implement storing and organising the data in dictionaries.
        print(Scraper.data)
        self.__get_picture()
        return Scraper.data #defined as a global variable. 
    
    def __get_picture(self):
        Image_info = self.driver.find_elements(By.XPATH,'//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div/div')
        #Accessing the image info using XPATH. Probably a cleaner way of doing this. 

        txt = Image_info[0].get_attribute("style")
        src = txt.split('"') #Only need the url so the code splits string at ". 
        url = src[1]
        name = Scraper.data[0]
        path = f'{name}.jpg' #Path is created from the first element of the list returned by 
                             #Summary Data. 
                             #Downloading image from url. 
        image = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(image)
        print(url)
        return(url)    

    def scrape(self):
        self.__accept_cookies()
        self.__enter_address(self.address)   ### Only works if 'mark location' button does not require the location pin to be moved
        self.__acknowledge_14_delivery()
