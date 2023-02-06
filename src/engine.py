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

        def __init__(self, trace, log, jsprms, dbcontext, driver, humanize, live_load, urls):
                self.trace = trace
                self.log = log
                self.jsprms = jsprms
                self.dbcontext = dbcontext
                self.driver = driver
                self.humanize = humanize
                self.live_load = live_load
                self.urls = urls
                self.root_app = os.getcwd()
                self.visited_this_session = list()

        def testit(self):
                print("teeet")
        
        # @_error_decorator
        def visit_users(self):
                self.trace(inspect.stack()) 
                base_url = self.urls.get_url('base')
                miniprofile = self.urls.get_url('miniprofile')              
                for profile in self.visited_this_session:  
                        url_profile = Template(miniprofile).substitute(base=base_url, profile=profile)                      
                        self.driver.get(url_profile)
                        visited = self.dbcontext.get_visited_obj()
                        visited.linkedin_id = profile.split('?')[0]
                        print(url_profile)
                        visited.date_visit = datetime.now()               
                        # print(visited)                        
                        self.dbcontext.add_to_visited(visited)
                        self.humanize.wait_human()

        # @_error_decorator
        def get_users_links(self):          
                self.trace(inspect.stack())       
                # elements = self.driver.find_elements(By.CSS_SELECTOR, ".entity-result__content");
                elements = self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
                print(len(elements))
                #div > span.entity-result__title-line > span')
                for el in elements:                        
                        href = el.find_element(By.TAG_NAME,'a').get_attribute('href')
                        print(href)                     
                        # https://www.linkedin.com/in/amine-haitouf-0a1993209?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADUBKbkB3Nx_C1AcKNObeuv-8SVf3_vMQyo                        
                        url = href.rsplit('/', 1)[1]
                        linkedin_id = url.split('?')[0]
                        # print(self.dbcontext.is_in_visited(url))
                        if not self.dbcontext.is_in_visited(linkedin_id) and not (url in self.visited_this_session): 
                                self.visited_this_session.append(url)
                

        # @_error_decorator
        def list_user_from_search(self):
                self.trace(inspect.stack()) 
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
        def do_search(self, keyword):
                self.trace(inspect.stack()) 
                sel_utils = self.live_load('utils.selenium_utils')
                element = self.driver.find_element(By.CSS_SELECTOR, '#global-nav-typeahead > input')
                sel_utils.type_onebyone(self.driver, self.humanize, element, keyword)
                element.send_keys(Keys.RETURN)
                self.humanize.wait_human(2,2)
                

        # @_error_decorator(False)  #il faut un false pour que l'appel marche en live load
        def search(self):
                self.trace(inspect.stack()) 

              
                self.driver.get(self.urls.get_url('base'))
                self.humanize.wait_human(2, 1)
                self.do_search("python")
                self.humanize.wait_human(2, 1)
                self.list_user_from_search()
                self.humanize.wait_human(3, 3)
                # self.dbcontext.session.rollback()
                nb_page = self.jsprms.prms['result_page_nb']                
                for i in range(nb_page):
                        self.get_users_links()                        
                        # wk = input("analyse (b to break) : ")
                        # if wk == 'b':
                        #        break
                        but_suivant = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Suivant']")                        
                        but_suivant.click()
                        self.humanize.wait_human(5, 5)
                for vis in self.visited_this_session:
                        print(vis)
                self.visit_users()
                
                


            