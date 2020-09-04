from utils import logIn, getNLID, getAuthor, nextPage, getRate, getDescription, tryFind, getIdFromUrl, clickButton
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from time import sleep
import random 
import time
import json 
import sys 
from tqdm import tqdm 

if __name__ == "__main__":

    # 1. Define browser
    # browser = webdriver.Chrome(executable_path='./chromedriver')
    browser = webdriver.Chrome(ChromeDriverManager().install())

    start = time.time()

    # 2. Open URL 
    url = "https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=30"
    browser.get(url)

    # 3. Login website
    logIn(browser)

    # 4-1. Get names, authors, links, ids, rates from root web pages
    names, authors, links, ids, rates, descriptions, reviews = [], [], [], [], [], [], []
    id_dictionary = {}

    flag = True 
    while flag:
        getNLID(browser, names, links, ids)
        getAuthor(browser, authors)
        getRate(browser, rates)
        flag = nextPage(browser, flag)
        # Wait browser load data 
        sleep(1)
        # sleep(random.randint(3, 5))
        # break
    
    n_books = len(ids)
    rate_txt2int = {'did not like it': 1, 'it was ok': 2, 'liked it': 3, 'really liked it': 4, 'it was amazing': 5}

    # 4-2. Get descriptions and reviews
    total_failed = 0
    for i_book in tqdm(range(n_books)):
        try:
            start_book_i = time.time()
            # browser.get("https://www.goodreads.com/book/show/10925246-t-i-l-b-t")

            browser.get(links[i_book])
            sleep(1)
            review_dict = {}

            # Load all pages of reviews by flag 
            flag, flag_des = True, True
            while flag:
                # Just need to get description and All Languages option one time.
                if flag_des:
                    getDescription(browser, descriptions)
                    flag_des = False
                
                    #############################################
                    ##       Select All Languages option       ##
                    #############################################

                    try:
                        element = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.ID, 'language_code'))
                    )
                    except:
                        browser.quit()
                        sys.exit()
                        raise RuntimeError("Can't wait more than 30 seconds in this page ...")

                    for option in element.find_elements_by_tag_name('option'):
                        if option.text == 'All Languages':
                            option.click() 
                            # Load all comments of this page 
                            sleep(3)
                            break
                
                #############################################
                ##            COMMENT BUTTON               ##
                #############################################
            
                review_list = browser.find_elements_by_xpath("//div[@class='friendReviews elementListBrown']")  
                for review in review_list:
                    # Because it just support more button and comment button, we choose comment button if we have it 
                    comment_button = review.find_elements_by_xpath(".//a[@onclick!='swapContent($(this));; return false;']")
                    load_view = False 
                    for button in comment_button:
                        button_text = button.text
                        if button_text != "comment":
                            clickButton(browser, button)
                            sleep(0.1)
                            if "comment" in button_text:
                                # print(button.text)
                                sleep(1)
                                load_view = True 
                                break

                    if load_view:
                        # we choose view comment button if we have it 
                        try:
                            view_cmt_button = review.find_element_by_xpath(".//a[@class='loadingLink']")
                            # view_cmt_button.click()
                            clickButton(browser, view_cmt_button)
                            sleep(1)
                        except NoSuchElementException:
                            continue
                        
                #############################################
                ##            MORE BUTTON                  ##
                #############################################
                
                review_frame = browser.find_element_by_id("reviews")
                more_button = review_frame.find_elements_by_xpath(".//a[@onclick='swapContent($(this));; return false;']")
                n_button = len(more_button)
                
                for i in range(n_button):
                    more_button = browser.find_elements_by_xpath("//a[@onclick='swapContent($(this));; return false;']")
                    actions = ActionChains(browser)
                    actions.move_to_element(more_button[i]).perform()
                    if more_button[i].text == "...more":
                        more_button[i].click()
                        sleep(0.1)
                
                #############################################
                ##      GET ALL REVIEWS WITH CONTENT       ##
                #############################################

                review_list = browser.find_elements_by_xpath("//div[@class='friendReviews elementListBrown']")  
                for review in review_list:
                    author_rev = tryFind(review, ".//a[@class='left imgcol']")
                    rate_el = tryFind(review, ".//span[@class=' staticStars notranslate']")
                    content_el = tryFind(review, ".//div[@class='reviewText stacked']")
                    date_el = tryFind(review, ".//a[@class='reviewDate createdAt right']")
                    frames_cmt_el = review.find_elements_by_xpath(".//div[@class='brown_comment']")

                    # Id author user 
                    id_user = None if author_rev is None else getIdFromUrl(author_rev.get_attribute("href"))
                    name_user = None if author_rev is None else author_rev.get_attribute("title") 
                    rate = None if rate_el is None else rate_txt2int[rate_el.get_attribute("title")]
                    content = None if content_el is None else content_el.text
                    date = None if date_el is None else date_el.text
                    if content[-7:] == " (less)":
                        content = content[:-7]
                    
                    cmts = []
                    # Collect name, id and text of each user comment
                    for el in frames_cmt_el:
                        try:
                            cmt_el = el.find_element_by_xpath(".//div[@class='xhr_comment_body']")
                            id_el = cmt_el.find_element_by_xpath(".//a")
                            text_el = cmt_el.find_elements_by_xpath(".//span")
                            id_user_cmt = getIdFromUrl(id_el.get_attribute("href"))
                            name_user_cmt = id_el.text
                            # Date is the last element
                            text_user_cmt = text_el[-2].text
                            cmts.append([id_user_cmt, name_user_cmt, text_user_cmt]) 
                        except NoSuchElementException:
                            continue
                    
                    review_dict[id_user] = {"Name": name_user, "Rate": rate, "Date": date, "Content": content, "Comment": cmts}

                #############################################
                ##     GET ALL REVIEWS WITH NO CONTENT     ##
                #############################################

                review_list = browser.find_elements_by_xpath("//div[@class='friendReviews elementListBrown notext']")  
                for review in review_list:
                    
                    author_rev = tryFind(review, ".//a[@class='user']")
                    rate_el = tryFind(review, ".//span[@class=' staticStars notranslate']")
                    date_el = tryFind(review, ".//a[@class='reviewDate']")

                    id_user = None if author_rev is None else getIdFromUrl(author_rev.get_attribute("href"))
                    name_user = None if author_rev is None else author_rev.get_attribute("title")
                    rate = None if rate_el is None else rate_txt2int[rate_el.get_attribute("title")]
                    content = ''
                    date = None if date_el is None else date_el.text
                    review_dict[id_user] = {"Name": name_user, "Rate": rate, "Date": date, "Content": content, "Comment": cmts}

                flag = nextPage(browser, flag)
                # Wait browser load data 
                sleep(random.randint(3, 5))
                # sleep(3)
                

            id_dictionary[ids[i_book]] = {"Book Name": names[i_book], "Author": authors[i_book], "Total Rate": rates[i_book],
                                          "Description": descriptions[i_book], "Link": links[i_book], "Review": review_dict}
            
            print(f"Running time of {names[i_book]} : {time.time()-start_book_i}")

        except Exception as e:
            print(f"Failed to collect data from {names[i_book]} ...")
            total_failed += 1
            id_dictionary[ids[i_book]] = {"Book Name": names[i_book], "Author": authors[i_book], "Total Rate": rates[i_book],
                                          "Description": descriptions[i_book], "Link": links[i_book], "Review": review_dict}
    
    print(f"Have {total_failed} books can not collect.")
    
    # 5. Save data to json file 
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(id_dictionary, outfile, indent=2, separators=(", ", ": "), ensure_ascii=False)

    # 6. Close URL
    browser.close()

    print("Total running time :", time.time() - start)
    