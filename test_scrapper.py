import scrapper
import unittest
from unittest.mock import patch
from selenium import webdriver
from models import Category

# Testing creating files and delete test
from os import path
import shutil


class TestUdemyScrapper(unittest.TestCase):

    def setUp(self):
        self.page = "http://www.udemy.com"

    def test_obtain_categories(self):
        """
        Check if it's possible to get categories
        """
        categories = scrapper.get_categories(self.page)
        self.assertIsNotNone(categories)

    def test_convert_category_info_to_object(self):
        """
        In this case, we will try to convert two hypotetical categories
        to category objects
        """

        class Pseudocategory:
            def __init__(self, content, text):
                self.elements = {}
                self.elements["href"] = content
                self.text = text

            def __getitem__(self, item):
                return self.elements[item]

        hyp_categories = [
            Pseudocategory('/courses/design/', "Disenito"),
            Pseudocategory('/courses/it-and-software/', "Compus")
        ]
        with patch('bs4.BeautifulSoup.select', return_value=hyp_categories):
            categories = scrapper.get_categories(self.page)
            self.assertEqual(len(categories), 2)
            self.assertEqual(type(categories["Compus"].maxpages), int)
            self.assertEqual(type(categories["Disenito"].maxpages), int)
            self.assertEqual(categories["Compus"].name, "Compus")
            self.assertEqual(categories["Disenito"].name, "Disenito")
            self.assertTrue(categories["Disenito"].maxpages > 1)
            self.assertTrue(categories["Compus"].maxpages > 1)

    def test_get_courses(self):
        """
        We check a category with 4 pages
        """
        c = Category("compus", "https://www.udemy.com/courses/development/")
        c.maxpages = 4
        browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
        browser.implicitly_wait(10)
        with patch('models.Category._get_datetime_now', return_value="test1"):
            c.get_courses(browser)
        self.assertTrue(path.exists("files_test1/courses_compus_1.csv"))
        self.assertTrue(path.exists("files_test1/courses_compus_2.csv"))
        self.assertTrue(path.exists("files_test1/courses_compus_3.csv"))
        self.assertTrue(path.exists("files_test1/courses_compus_4.csv"))
        self.assertFalse(path.exists("files_test1/courses_compus_5.csv"))
        shutil.rmtree("files_test1")


if __name__ == '__main__':
    unittest.main()
