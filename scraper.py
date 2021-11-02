
from selenium import webdriver
from selenium.webdriver.common.by import By #\importing necessary modules.
from time import sleep
import requests

class Scraper:
    
 
    data = []
    def __init__(self) -> None: #initialising Selenium and starting the webdriver.
        self.driver = webdriver.Chrome()

    def __accept_cookies(self):
        # TODO
        pass
    
    def __enter_address(self, address):
        # TODO
        pass
    
    def __acknowledge_voucher(self):
        # TODO
        pass
    
    def __sort_page(self, option):
        # TODO
        pass

    def getSummary(self):
        Summary_info = self.driver.find_elements(By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div/div[1]')

        for info in Summary_info: #Looping over list of summary information about the restaraunt.     
            text = info.text
            Scraper.data = text.splitlines()
            #splits the string at new lines and stores as a list. 
            #at some point, we need to implement storing and organising the data in dictionaries.
        print(Scraper.data)
        self.getPicture()
        return Scraper.data #defined as a global variable. 
    
    def getPicture(self):
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
        #launches web browser and calls the next method. 
        self.driver.get(
        "https://deliveroo.co.uk/menu/london/fulham/mamino-fulham?day=today&geohash=gcpuuw8wdq1m&time=ASAP")
        self.getSummary()

Deliveroo_Scraper = Scraper()

Deliveroo_Scraper.scrape()

# %%
