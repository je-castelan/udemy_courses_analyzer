Udemy courses analizer
==============

In order to practice my data enginering knowledge, I'm making a web scapper which checks all the couses on Udemy and notify when a course is cheaper or more expensive than the last day.

Selenium driver
===============

It's important to download chromedriver and add the executable to the project. You can download it [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Instructions
============

# Udemy analizer

 - Create a virtual environment (python -m env venv)
 - Access to the virtual environment (source ~/env/bin/activate)
 - Execute "pip install -r requirements.txt"
 - Execute "python scrapper.py"
 - You will see than 15 google windows will open to execute scrapping. Don't worry!

It will generate a folder caller `files_YYYY_MM_DD` with the current date. Into the folder, you will check all the caouses in every page on Udemy.