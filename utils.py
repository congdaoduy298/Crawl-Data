from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

def sendKeys(browser):
    email = browser.find_element_by_id("user_email")
    email.send_keys("huynhquynh1123@gmail.com")

    password = browser.find_element_by_id("user_password")
    password.send_keys("123456@")
    password.send_keys(Keys.ENTER)

def logIn(browser):
    topButton = browser.find_elements_by_xpath("//a[@class='siteHeader__topLevelLink']")
    for button in topButton:
        if button.text == "Sign In":
            sign_in = button
            sign_in.click()
            sleep(3)
            sendKeys(browser) 
            break 

def getNLID(browser, names, links, ids):
    book_list = browser.find_elements_by_xpath("//a[@class='bookTitle']")
    for book in book_list:
        link = book.get_attribute("href")
        links.append(link)
        names.append(book.text)
        ids.append(link.split('/')[-1].split('-')[0])

def getAuthor(browser, authors):
    # Find author span 
    authors_list = browser.find_elements_by_xpath("//span[@itemprop='author']")
    for auts in authors_list:
        authors.append(auts.text)

def getRate(browser, rates):
    rates_list = browser.find_elements_by_xpath("//span[@class='minirating']")
    for rate in rates_list:
        rates.append(rate.text.split('\n')[-1])

def getDescription(browser, descriptions):
    # Find more button
    more_button = browser.find_element_by_xpath("//a[@onclick='swapContent($(this));; return false;']")
    more_button.click()
    description = browser.find_element_by_xpath("//div[@id='description']")
    descriptions.append(description.text[:-7])
    

def nextPage(browser, flag):
    next_page = browser.find_elements_by_xpath("//a[@class='next_page']")
    if len(next_page) == 0:
        return False
    else: 
        next_page[0].click()
    return True
