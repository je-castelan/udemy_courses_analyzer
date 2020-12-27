import bs4
import requests
from selenium import webdriver
import threading
import logging

from models.ScrappingCourses import ScrappingCourses
from models.Course import Course

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_categories(webpage):
    """
    In this page, we get the main categories of the webpage inserted
    """
    logging.info('Start accessing to {} to get the categories'.format(webpage))
    response = requests.get(webpage)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    categories = soup.select('.category-card--category-card-title-link--3PqTy')
    dict_categories = {}
    for category in categories:
        dict_categories[category.text] = category['href']
    logging.info('Categories obtanied. {} categories in total'.format(len(dict_categories)))
    return dict_categories

def _get_pages_on_category(web_category, browser):
    """
    Accesing to tjhe main page of category, it returns the max page of the category
    """
    browser.get(web_category)
    pages = browser.find_elements_by_class_name("pagination--page--3FKqV")
    return int(pages[-1].text)


def get_pages_all_categories(categories):
    """
    On the categories on the list, it returns all the pages to consult
    """
    logger.info("Checking pages on categories")
    list_pages = []
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
    browser.implicitly_wait(10)
    for category, web_category in categories.items():
        maxpage = _get_pages_on_category(web_category, browser)
        list_pages += [(category, "{}?p={}".format(web_category,i)) for i in range(1, maxpage + 1)]
        logger.info("Category {} has {} pages".format(category, maxpage))
    browser.close()
    logger.info("Total pages are {}".format(len(list_pages)))
    return list_pages

def _divide_pages_list(pages):
    """
    It divided the list pages on a list of lists to be managed with threads
    """
    divided_pages = []
    parts = 15
    size = len(pages) // parts
    for i in range (0, len(pages), size):
        divided = [pages[j] for j in range(i,i+size if i+size < len(pages) else len(pages))]
        divided_pages.append(divided)
    return divided_pages

def counter(scrappers, total):
    """
    Fucntion which check the pages checked
    """
    ready = 0
    while ready < total:
        newready = 0
        for scrapper in scrappers:
            newready += scrapper.ready
        if newready != ready:
            ready = newready
            logger.info("Status {}/{} scrapped".format(ready,total))
    logger.info("Scrapping ready")

if __name__ == "__main__":
    """
    Main function
    """ 
    page = "http://www.udemy.com"
    categories = {k: page + v for k, v in get_categories(page).items()}
    pages = get_pages_all_categories(categories)
    pages_divided = _divide_pages_list(pages)
    threads = list()
    for i in range(len(pages_divided)):
        scrapingcourses = ScrappingCourses(pages_divided[i])
        t = threading.Thread(target=scrapingcourses.get_courses_of_pages)
        threads.append(scrapingcourses)
        t.start()
    c = threading.Thread(target=counter, args=(threads, len(pages)))
    c.start()