# -*-coding:utf-8 -*
import os
from os import path
import inspect
from datetime import datetime
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from string import Template
#mes libs
import utils.str_utils as str_utils
import utils.file_utils as file_utils
from utils.urls import Urls
from utils.mydecorators import _error_decorator
from utils.selenium_utils import type_onebyone


class Engine:

        def __init__(self, trace, log, jsprms, driver, humanize,  urls):
                self.trace = trace
                self.log = log
                self.jsprms = jsprms
                self.driver = driver
                self.humanize = humanize
                self.urls = urls
                self.root_app = os.getcwd()
                self.visited_this_session = list()

        def testit(self):
                print("test0eet")
        
        @_error_decorator(False)
        def search(self):
                search_button = self.driver.find_element(By.CSS_SELECTOR,'#global-nav-search > div > button')
                search_button.click()
                self.humanize(1,2)
                element = self.driver.find_element(By.CSS_SELECTOR, '#global-nav-typeahead > input')
                type_onebyone(self.driver, self.humanize, element, 'python')



            