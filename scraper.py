from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from uuid import uuid4
from logger import log

import requests
import time
import os
import json

class Scraper:
    """
    This class is used to scrape data from Deliveroo.
    
    Attributes:
    Address (string): The postcode of the area of restaurants to be scraped. 
    """
    def __init__(self, address: str, existing_data=[], output_loc=None) -> None:
        """
        See help(Scraper) for accurate signature.
        """
        options = Options()
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920,1080')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://deliveroo.co.uk')
        time.sleep(4)
        self.address = address
        self.existing_data = existing_data
        self.dataoutput = output_loc
        if output_loc is None:
            self.dataoutput = f'data/{address}'
    
    def _accept_cookies(self):
        WebDriverWait(self.driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
        ).click()

    def _enter_address(self, address):
        self.addressbar = self.driver.find_element(By.XPATH, '//*[@id="location-search"]')
        self.addressbar.send_keys(f'{address}')
        self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/span/button').click()
        try:
            WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/span/button'))
            ).click()
        except:  #if map location does not show 
            pass
        # TODO: this needs some work!
        # try:
        #     WebDriverWait(self.driver, 2).until(
        #         EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[1]/div/div/div/div/a'))
        #     )
        # except:
        #     raise ValueError('Sorry! Deliveroo does not operate in this area, try a different address!')
        
    
    def _acknowledge_popups(self):
        # find the "Ok" button in acknowledgement pop ups
        time.sleep(1.5)
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[8]/div/div/div/div/div/div[2]/span[2]/button').click()
        except:
            pass
        try:
            self.driver.find_element(By.XPATH,'/html/body/div[9]/div/div/div/div/div/div[2]/span[2]/button').click()
        except:
            pass
        try:
            modals = self.driver.find_elements(By.XPATH, '//div[starts-with(@class, "ReactModalPortal")]')
            for modal in modals:
                self.driver.execute_script("arguments[0].style.display = 'none';", modal)
        except Exception as e:
            log('error', f'Unable to hide modals: {e}')
            
    def _sort_page(self, option: str='rating'):
        options = ['time', 'rating', 'hygiene', 'distance']
        if option in options:
            self.driver.get(f'{self.driver.current_url}&sort={option}')
        
    def _collect_restaurants(self, limit: int=None):
        try:
            res_menu = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div[2]/div/ul'))
            )
        except Exception as e:
            log('error', f'Unable to find restaurants container {e}')
            return []
        res_list = res_menu.find_elements(By.TAG_NAME,'li')
        urls = []
        for res in res_list:
            try:
                if limit is not None and len(urls) >= limit:
                    break
                el = res.find_element(By.TAG_NAME,'a')
                try:
                    res_name = el.find_element(By.TAG_NAME, 'p').text
                except Exception as e:
                    log('error', f'Unable to get restaurant from card {e}')
                    res_name = ''
                res_url = el.get_attribute('href')
                urls.append((res_name,res_url))
            except Exception as e:
                pass
        return urls

    def _get_summary(self):
        data = {}
        try:
            # Image on the right side of the page and description on the left
            container = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app-element"]/div/div[2]/div[1]/div[2]/div'))
            )
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
            container = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/div/div'))
            )
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
        path = f'{self.dataoutput}/images/{str(uuid4())}.jpg'
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

    def scrape(self, num):
        """
        This function calls private members of the scrape class and returns data on restaurants on deliveroo.
        
        Returns:
        Dictionary of scraped data and jpgs of the restaurants.
        """
        log('info', f'Starting {num} restaurants scraping at address {self.address}')
        log('info', 'Stage 1: accepting cookies...')
        self._accept_cookies()
        log('info', f'Stage 2: entering address {self.address}')
        self._enter_address(self.address)
        log('info', 'Stage 3: close any promotional pop ups')
        self._acknowledge_popups()
        log('info', 'Stage 4: sort restaurants...')
        self._sort_page()
        time.sleep(10)
        log('info', f'Stage 5: collect {num} restaurants...')
        urls = self._collect_restaurants(num)
        restaurants = self.existing_data
        log('info', f'Stage 6: Scraping each collected {len(urls)} restaurant...')
        for i, (name, url) in enumerate(urls):
            log('info', f'{i + 1}: Attempting to scrape {name}')
            if url in restaurants.__str__():
                log('info', 'Restaurant already exists, skipping...')
                continue
            try:
                self.driver.get(url)
                try:
                    data = self._get_summary()
                    data['uuid'] = str(uuid4())
                    data['url'] = url
                    restaurants.append(data)
                except Exception as e:
                    log('error', f'Unable to scrape restaurant page {url}: {e}')
            except Exception as e:
                log('error', f'Unable to open page {url}: {e}')
        return restaurants