from selenium.webdriver.common.keys import Keys 
from selenium import webdriver 
from utils import logIn, getNLID, getAuthor, nextPage
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

    # 4. Get names, authors, links, ids from web
    names, authors, links, ids = [], [], [], []
    flag = True 
    while flag:
        getNLID(browser, names, links, ids)
        getAuthor(browser, authors)
        flag = nextPage(browser, flag)
        # Wait browser load data 
        sleep(random.randint(3, 6))

    # 5. Save data to csv
    arr = np.asarray([ids, names, authors, links]).T
    header = ['Id', 'Name', 'Authors', 'Link']
    pd.DataFrame(arr).to_csv('myDatabase.csv', header=header, index=False)
    
    # 6. Close URL
    browser.close()