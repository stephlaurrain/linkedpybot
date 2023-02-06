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

        def __init__(self, trace, log, jsprms, driver, humanize, live_load, urls):
                self.trace = trace
                self.log = log
                self.jsprms = jsprms
                self.driver = driver
                self.humanize = humanize
                self.live_load = live_load
                self.urls = urls
                self.root_app = os.getcwd()
                self.visited_this_session = list()

        def testit(self):
                print("teeet")
        
        # @_error_decorator
        def get_users_links(self):
                elements = self.driver.find_elements(By.CSS_SELECTOR, 'div > span.entity-result__title-line > span')
                for el in elements:                        
                        href = el.find_element(By.TAG_NAME,'a').get_attribute('href') 
                        print(href)         
                # self.driver.get(href)

        # @_error_decorator
        def list_user_from_search(self):
                elements = self.driver.find_elements(By.CSS_SELECTOR, 'div > div.search-results__cluster-bottom-banner')
                search_url = ''
                for el in elements:                    
                        href = el.find_element(By.TAG_NAME,'a').get_attribute('href')    
                        if '/search/results/people' in href:
                                search_url = href
                                print('found')
                                break; 
                self.driver.get(search_url)

        # @_error_decorator
        def do_search(self):
                sel_utils = self.live_load('utils.selenium_utils')
                element = self.driver.find_element(By.CSS_SELECTOR, '#global-nav-typeahead > input')
                sel_utils.type_onebyone(self.driver, self.humanize, element, 'python')
                element.send_keys(Keys.RETURN)
                self.humanize.wait_human(2,2)
                

        # @_error_decorator(False)  #il faut un false pour que l'appel marche en live load
        def search(self):
                
                
                self.driver.get(self.urls.get_url('base'))
                self.humanize.wait_human(2, 1)
                
                self.do_search()
                self.list_user_from_search()
                self.get_users_links()
                # print(elements)
                #\35 ebORYRqQSWZmsaipq3WmQ\=\= > div > div.search-results__cluster-bottom-banner.artdeco-button.artdeco-button--tertiary.artdeco-button--muted > a
                #sel_utils.do_click(element)
                
                


            