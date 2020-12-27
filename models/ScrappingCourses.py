from selenium import webdriver
import logging
import os
import csv
import datetime
from selenium.common.exceptions import NoSuchElementException

from models.Course import Course

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScrappingCourses:

    def __init__(self, pages):
        self.pages = pages
        self.pending = len(pages)
        self.ready = 0

    def get_courses_of_pages(self):
        """
        It access to the pages on the list to check all the courses
        """
        browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
        browser.implicitly_wait(10)
        for category, page in self.pages:
            self.get_courses(category, page, browser)
            self.ready += 1
            self.pending -= 1
        browser.close()

    def get_courses(self, category, page, browser):
        """
        It generates the file with the couses on a page
        """
        tries = 0
        done = False
        clean_courses = []
        while not done:
            try:
                browser.get(page)
                courses = browser.find_elements_by_class_name("browse-course-card--link--3KIkQ")
                for course in courses:
                    url = course.get_attribute("href")
                    detail = course.find_element_by_class_name("course-card--large--1BVxY")
                    name = detail.find_element_by_class_name("udlite-focus-visible-target").text
                    prize = detail.find_element_by_class_name("price-text--price-part--Tu6MH").text.split("\n")[1]
                    rank = detail.find_element_by_class_name("course-card--row--1OMjg").find_element_by_class_name("star-rating--rating-number--3lVe8").text
                    c = Course(category, name, prize, url, rank)
                    clean_courses.append(c)
                self._save_courses(category, page.split("=")[1], clean_courses)
                done = True
            except NoSuchElementException as ne:
                tries += 1
                logger.warning('Page {} is having troubles. Tried {}/3'.format(page, tries))
                if tries >= 3:
                    done = True
                    logger.error('Page {} failed.'.format(page))
        return done

    def _get_datetime_now(self):
        """
        Function which returns a string with the current datetime with formar YYYY_MM_DD
        """
        return datetime.datetime.now().strftime('%Y_%m_%d')

    def _save_courses(self,category, page, courses):
        """
        It generates the file with the obtained courses on a pages 
        """
        now = self._get_datetime_now()
        if not os.path.exists('files_{}'.format(now)):
            os.makedirs('files_{}'.format(now))
        out_file_name = 'files_{}/courses_{}_{}.csv'.format(now,category,page)
        csv_headers = list(filter(lambda property: not property.startswith('_'), dir(courses[0])))
        with open(out_file_name, mode='w+', encoding='utf-8', newline='') as f:
            writer =  csv.writer(f)
            writer.writerow(csv_headers)
            for course in courses:
                row = [str(getattr(course, prop)) for prop in csv_headers]
                writer.writerow(row)
