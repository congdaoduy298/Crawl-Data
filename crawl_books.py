from selenium.webdriver.common.keys import Keys 
from selenium import webdriver 
from utils import logIn, getNLID, getAuthor, nextPage, getRate, getDescription
from time import sleep
import pandas as pd 
import numpy as np 
import random 
import os 


if __name__ == "__main__":
    # 1. Define browser
    browser = webdriver.Chrome(executable_path='./chromedriver')

    # 2. Open URL 
    url = "https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=30"
    browser.get(url)

    # 3. Login website
    logIn(browser)

    # 4-1. Get names, authors, links, ids, rates from root web pages
    names, authors, links, ids, rates, descriptions = [], [], [], [], [], []
    flag = True 
    while flag:
        getNLID(browser, names, links, ids)
        getAuthor(browser, authors)
        getRate(browser, rates)
        flag = nextPage(browser, flag)
        # Wait browser load data 
        sleep(random.randint(3, 6))
        break
    
    # 4-2. Get descriptions
    for i in range(len(names)):
        browser.get(links[i])
        getDescription(browser, descriptions) 
        sleep(random.randint(3, 5))

    # 5. Save data to csv
    arr = np.asarray([ids, names, authors, rates, links, descriptions]).T
    header = ['Id', 'Name', 'Authors', 'Rate', 'Link', 'Description']
    pd.DataFrame(arr).to_csv('myDatabase.csv', header=header, index=False)
    
    # 6. Close URL
    browser.close()