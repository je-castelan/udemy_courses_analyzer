import logging
import os
import csv
import datetime
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Category:
    def __init__(self, name, url, browser=None):
        self.name = name
        self.url = url
        logging.info("Checking category {} in url {}".format(
            self.name,
            self.url
            )
        )
        if browser:
            browser.get(self.url)
            self.maxpages = int(browser.find_elements_by_class_name(
                "pagination--page--3FKqV"
                )[-1].text)
        else:
            self.maxpages = 1
        self.pending = self.maxpages
        self.ready = 0

    def get_courses(self, browser):
        """
        It generates the file with the couses on a page
        """
        logger.info("Checking pages on category {}".format(self.name))
        for i in range(1, self.maxpages + 1):
            tries = 0
            done = False
            clean_courses = []
            while not done:
                if not os.path.exists("files_{}/courses_{}_{}.csv".format(
                    self._get_datetime_now(),
                    self.name,
                    i)
                ):
                    try:
                        browser.get("{}?p={}".format(self.url, i))
                        courses = browser.find_elements_by_class_name(
                            "browse-course-card--link--3KIkQ"
                            )
                        for course in courses:
                            url = course.get_attribute("href")
                            detail = course.find_element_by_class_name(
                                "course-card--large--1BVxY"
                                )
                            name_course = detail.find_element_by_class_name(
                                "udlite-focus-visible-target"
                                ).text
                            prize = detail.find_element_by_class_name(
                                "price-text--price-part--Tu6MH"
                                ).text.split("\n")[1]
                            rank = detail.find_element_by_class_name(
                                "course-card--row--1OMjg"
                                ).find_element_by_class_name(
                                    "star-rating--rating-number--3lVe8"
                                    ).text
                            c = Course(
                                self.name,
                                name_course,
                                prize,
                                url,
                                rank
                                )
                            clean_courses.append(c)
                        self._save_courses(self.name, i, clean_courses)
                        done = True
                    except NoSuchElementException:
                        tries += 1
                        logger.warning(
                            'Page {} on {} tried {}/5'.format(
                                i,
                                self.name,
                                tries
                                )
                            )
                        if tries >= 5:
                            done = True
                            logger.error('Page {} on {} failed.'.format(
                                i,
                                self.name
                                )
                                )
                else:
                    done = True
            self.ready += 1
        browser.close()

    def _get_datetime_now(self):
        """
        Function which returns a string with the current
        datetime with formar YYYY_MM_DD
        """
        return datetime.datetime.now().strftime('%Y_%m_%d')

    def _save_courses(self, category, page, courses):
        """
        It generates the file with the obtained courses on a pages
        """
        now = self._get_datetime_now()
        if not os.path.exists('files_{}'.format(now)):
            os.makedirs('files_{}'.format(now))
        out_file_name = 'files_{}/courses_{}_{}.csv'.format(
            now,
            category,
            page
            )
        csv_headers = list(filter(
            lambda property: not property.startswith('_'),
            dir(courses[0])))
        with open(out_file_name, mode='w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)
            for course in courses:
                row = [str(getattr(course, prop)) for prop in csv_headers]
                writer.writerow(row)


class Course:
    def __init__(self, category, name, prize, url, rank):
        self._category = category
        self._name = name
        self._prize = prize
        self._url = url
        self._rank = rank

    @property
    def category(self):
        return self._category

    @property
    def name(self):
        return self._name

    @property
    def prize(self):
        return self._prize

    @property
    def url(self):
        return self._url

    @property
    def rank(self):
        return self._rank

    def __str__(self):
        return "Curso {} en categoria {} a {}".format(
            self.name,
            self.category,
            self.prize
            )
