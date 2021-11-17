from selenium import webdriver
from selenium.webdriver.common.by import By
from uuid import uuid4

import requests
import time

class Scraper:
    """
    This class is used to scrape data from Deliveroo.
    
    Attributes:
    Address (string): The postcode of the area of restaurants to be scraped. 
    """
    def __init__(self, address: str) -> None:
        """
        See help(Scraper) for accurate signature.
        """
        self.driver = webdriver.Chrome()
        self.driver.get('https://deliveroo.co.uk')
        self.address = address

    def __accept_cookies(self):
        time.sleep(1.5)   ##could have a shorter sleep time
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
        
    
    def __acknowledge_popups(self):
        # find the "Ok" button in acknowledgement pop ups
        time.sleep(1.5)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[8]/div/div/div/div/div/div[2]/span[2]/button').click()
            
        except:
            pass
             
    def __sort_page(self, option: str='Top_rated'):
        if option not in self.sort_options:
            raise ValueError("Option does not exist")
        try:
            self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/button').click()
            filter_list = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div[1]/div/div[1]/div/div[2]/div[1]/div/div/ul')
            
            sort_options = {
                'Distance': 0,
                'Hygiene_ratings': 1,
                'Recommended': 2,
                'Time': 3,
                'Top_rated': 4
            }
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
        data = {}
        try:
            # Image on the right side of the page and description on the left
            container = self.driver.find_element(By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div')
            subcontainers = container.find_elements(By.XPATH, './div')
            header = subcontainers[0].find_element(By.XPATH, './div')
            image_container = subcontainers[1]
            
            data['rating'] = header.find_element(By.XPATH, './div').text.split('(')[0]
            
            tags_list = header.find_element(By.XPATH, './div/ul')
            tags = tags_list.find_elements(By.TAG_NAME, 'li')
            tags = [tags.text for tags in tags]
            
            image = image_container.find_element(By.XPATH, './div/div/div')
        except:
            # Image on the left side of the page and description on the right
            container = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div/div/div[2]')
            subcontainers = container.find_elements(By.XPATH, './div')
            image_container = subcontainers[0]
            header = subcontainers[1]

            tag_containers = header.find_elements(By.TAG_NAME, 'p')
            tag_containers = tag_containers[:-1] # Ignore 'Info'
            tags = []
            for tag_container in tag_containers:
                tags_list = tag_container.find_elements(By.XPATH, './span')
                tags += [tag.text for tag in tags_list if tag.text != '·' and tag.text != '']
            
            image = image_container.find_element(By.XPATH, './div')
            
        data['tags'] = tags
        data['name'] = header.find_element(By.TAG_NAME, 'h1').text
        
        url = self.__get_picture_url(image)
        path = f'{str(uuid4())}.jpg'
        data['image_path'] = path
        self.__save_image(url, path)
        
        return data
    
    def __save_image(self, url: str, path: str):
        image = requests.get(url).content
        with open(path,'wb') as f:
            f.write(image)
    
    def __get_picture_url(self, image=None):
        if image is None:    
            try:
                Image_info = self.driver.find_elements(By.XPATH,'//*[@class = "restaurant__image"]//*')
                txt = Image_info[1].get_attribute("style")
            except:
                Image_info = self.driver.find_elements(By.XPATH,'//*[@class = "MenuHeader-cf659db292cfad50"]/*')
                txt = Image_info[0].get_attribute("style")
            
            src = txt.split('"') #Only need the url so the code splits string at ". 
            url = src[1]
            return url
        
        url = image.value_of_css_property('background-image')
        url = url.replace('url("', '').replace('")', '')
        return url

    def scrape(self):
        """
        This function calls private members of the scrape class and returns data on restaurants on deliveroo.
        
        Returns:
        Dictionary of scraped data and jpgs of the restaurants.
        """
        self.__accept_cookies()
        self.__enter_address(self.address)
        self.__acknowledge_popups()
        self.__sort_page()
        time.sleep(5)
        urls = self.__collect_restaurants(2)
        restaurants = []
        for (name, url) in urls:
            self.driver.execute_script(f"window.open('{url}', '_blank');")
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(5)
            data = self.__get_summary()
            data['uuid'] = uuid4()
            data['url'] = url
            restaurants.append(data)
        return restaurants