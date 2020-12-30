import bs4
import requests
from selenium import webdriver
import threading
import logging
import argparse

from models import Category

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_categories(webpage, limit_pages):
    """
    In this page, we get the main categories of the webpage inserted
    """
    logging.info('Start accessing to {} to get the categories'.format(webpage))
    response = requests.get(webpage)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    categories = soup.select('.category-card--category-card-title-link--3PqTy')
    dict_categories = {}
    browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
    browser.implicitly_wait(10)
    for category in categories:
        name = category.text
        dict_categories[name] = Category(
            name,
            webpage + category['href'],
            limit_pages,
            browser
            )
    logging.info('Categories obtanied. {} categories in total'.format(
        len(dict_categories)))
    browser.close()
    return dict_categories


def counter(categories, total):
    """
    Fucntion which check the pages checked
    """
    ready = 0
    while ready < total:
        newready = 0
        for category in categories:
            newready += category.ready
        if newready != ready:
            ready = newready
            logger.info("Status {}/{} scrapped".format(ready, total))
    logger.info("Scrapping ready")


if __name__ == "__main__":
    """
    Main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pages",
        help="Give a page limit to consult for every category",
        type=int)
    page = "http://www.udemy.com"
    args = parser.parse_args()
    if not args.pages:
        logger.error("Page limit is not defined. Finishing")
        print("It's mandatory to assign a page limit")
    else:
        categories = get_categories(page, args.pages)
        threads = list()
        maxpages = 0
        for category, objCategory in categories.items():
            logger.info("Opening browser to check {} category".format(
                category
                ))
            maxpages += objCategory.maxpages
            browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
            browser.implicitly_wait(10)
            t = threading.Thread(
                target=objCategory.get_courses,
                args=(browser,)
                )
            threads.append(objCategory)
            t.start()
        c = threading.Thread(target=counter, args=(threads, maxpages))
        c.start()
