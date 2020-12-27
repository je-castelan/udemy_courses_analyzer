import scrapper
import unittest
import datetime
from unittest.mock import patch
import threading

from models.ScrappingCourses import ScrappingCourses
from models.Course import Course

# Testing creating files and delete test
from os import path
import shutil

class TestScrapper(unittest.TestCase):

    def test_pages_obtention(self):
        """
        This test check if it's getting a array with tuples with the pages to get courses
        """
        categories = {
            "Personal":"https://www.udemy.com/courses/personal-development/", 
            "Bisnes": "https://www.udemy.com/courses/business/",
            }
        pages = scrapper.get_pages_all_categories(categories)
        self.assertEqual(tuple,type(pages[0]))

    def test_courses_obtention(self):
        """
        This page test 2 pages to obtain couses
        """
        pages = [
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=605'),
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=606'),
            ]
        with patch('models.ScrappingCourses.ScrappingCourses._get_datetime_now', return_value = "test1"):
            s = ScrappingCourses(pages)
            s.get_courses_of_pages()
        self.assertTrue(path.exists("files_test1/courses_Bisnes_605.csv"))
        self.assertTrue(path.exists("files_test1/courses_Bisnes_606.csv"))
        self.assertFalse(path.exists("files_test1/courses_Bisnes_607.csv"))
        shutil.rmtree("files_test1")
        
    
    def test_obtain_pages(self):
        categories = {
            "Personal":"https://www.udemy.com/courses/personal-development/", 
            "Bisnes": "https://www.udemy.com/courses/business/",
            "Music": "https://www.udemy.com/courses/music/",
            }
        with patch('scrapper._get_pages_on_category') as paging:
            paging.side_effect = [4,6,3]
            pages = scrapper.get_pages_all_categories(categories)
            self.assertEqual(len(pages),13)

    def test_counter(self):
        pages = [
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=505'),
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=506'),
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=507'),
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=508'),
            ('Bisnes', 'https://www.udemy.com/courses/business/?p=509'),
            ]
        with patch('models.ScrappingCourses.ScrappingCourses._get_datetime_now', return_value = "test2"):
            threads = []
            s = scrapper.ScrappingCourses(pages)
            s.get_courses_of_pages()
            t = threading.Thread(target=s.get_courses_of_pages)
            threads.append(s)
            t.start()
            c = threading.Thread(target=scrapper.counter, args=(threads, len(pages)))
            c.start()
        shutil.rmtree("files_test2")
        

if __name__ == '__main__':
    unittest.main()