#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime

#User Agent
from fake_useragent import UserAgent
import requests
import random
from pprint import pprint
from fake_useragent import UserAgent
from collections import OrderedDict

#BS4
from bs4 import BeautifulSoup


# In[11]:


import os
os.getcwd()


# In[9]:


os.environ['GH_TOKEN'] = ""

    
df_temp = pd.DataFrame()

#Reading sample input
input_products = pd.read_csv("/home/ubuntu/Shubham/hg_insights/SubCat_description_from_hg/input/HgInsights_subcat_final_nodupe.csv")
for index,row in input_products.iterrows():
    templist = []
    category_name = row[0]
    category_url = row[1]
    try:
        #Initiating driver and loading HGinsights
        firefox_options = FirefoxOptions()
        firefox_options.headless = True
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile() 
        profile_2 = profile.set_preference("general.useragent.override", useragent.random)
        driver = webdriver.Firefox(options=firefox_options ,firefox_profile=profile_2, service=Service(GeckoDriverManager().install()))
        driver.set_page_load_timeout(60)
        print(profile)
        print(useragent)
        driver.get(category_url)
        driver.maximize_window()
        #//div/div[2][contains(@class, 'collection-details-description')
        #Sub - Category  Description
        try:
            #//div/div[2][contains(@class, 'collection-details-description')]
            sub_cat_description = driver.find_element(By.XPATH, "//div/div[2][contains(@class, 'collection-details-description')]").text
            #print(sub_cat_description)
        except:
            sub_cat_description = " "
            print("sub_cat_description Not Found")
        #Products under sub category and product url
        #//li/a[contains(@class, 'default-link')]
        card_list = []
        all_products = driver.find_elements(By.XPATH, "//li/a[contains(@class, 'default-link')]")
        for prod in all_products:
            #product name
            try:
                product_name = prod.text
            except:
                product_name = " "
                print("product name not found")
            #product url
            #
            try:
                product_url = prod.get_attribute('href')
            except:
                product_url = " "
                print("product_url not found")
            print(f"{category_name}, {category_url}, {sub_cat_description}")
            table_dict = {'category_name': category_name, 'category_url': category_url, 'sub_cat_description': sub_cat_description, 'product_name': product_name, 'product_url': product_url}
            templist.append(table_dict)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
        time.sleep(60)
    else:
        df_temp = pd.DataFrame(templist)
        df_temp.to_csv(f"/home/ubuntu/Shubham/hg_insights/SubCat_description_from_hg/output/{category_name}.csv", index=False)
        driver.quit()
        time.sleep(2)
        


# In[ ]:




