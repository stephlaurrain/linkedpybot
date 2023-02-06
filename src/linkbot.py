# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep
import inspect
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import utils.file_utils as file_utils
import utils.mylog as mylog
import utils.jsonprms as jsonprms
import utils.img_utils as img_utils
from utils.humanize import Humanize
from dalib.dbcontext import Dbcontext
from utils.urls import Urls
from utils.selenium_utils import is_driver_on
from utils.mydecorators import _error_decorator
from selenium.webdriver.common.action_chains import ActionChains
import importlib

def test():
        print('tes')

class Bot:
      
        def __init__(self):                
                self.driver = None

        def trace(self,stck):                
                self.log.lg(f"{stck[0].function} ({ stck[0].filename}-{stck[0].lineno})")

        # init
        @_error_decorator()
        def init_webdriver(self):
                self.trace(inspect.stack())
                if self.driver != None:
                        return 
                options = webdriver.ChromeOptions()
                if (self.jsprms.prms['headless']):
                        options.add_argument("--headless")
                else:
                        options.add_argument("user-data-dir=./chromeprofile")
                # anti bot detection
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                # pi / docker
                if (self.jsprms.prms['box']):
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-gpu")
                        prefs = {"profile.managed_default_content_settings.images": 2}
                        options.add_experimental_option("prefs", prefs)
                # options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)                                  
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resolve the unreachable
                driver.set_window_size(1900, 1080)
                # driver.set_window_position(0, 0, windowHandle=) #, windowHandle='current')
                driver.maximize_window()
                driver.implicitly_wait(self.jsprms.prms['implicitly_wait'])
                self.driver = driver
        
        @_error_decorator()
        def get_db_context(self, param):
                self.trace(inspect.stack())
                dbcontext = Dbcontext(self.log)
                dbpath = f"{self.root_app}{os.path.sep}data{os.path.sep}database{os.path.sep}{param}"
                dbcontext.set_dbpath(dbpath)
                dbcontext.connect()
                return dbcontext

        @_error_decorator()
        def remove_logs(self):
                self.trace(inspect.stack())
                keep_log_time = self.jsprms.prms['keep_log_time']
                keep_log_unit = self.jsprms.prms['keep_log_unit']
                self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)                        
        
        def init_main(self, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack())
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"                        
                        self.jsprms = jsonprms.Prms(jsonFn)                        
                        self.test = self.jsprms.prms['test']
                        self.login = self.jsprms.prms['login']
                        self.password = self.jsprms.prms['password']
                        self.log.lg("=HERE WE GO=")                        
                        self.remove_logs()
                        self.dbcontext = self.get_db_context(self.jsprms.prms['dbpath'])
                        self.log.lg(f"Visited so far {self.dbcontext.visited_count()}")
                        self.log.lg("=Here I am=")                                                  
                          
                except Exception as e:
                        self.log.errlg(f"Wasted ! : {e}")
                        raise

        def newtab(self,url):         
                self.trace(inspect.stack())   
                self.driver.execute_script("window.open('{0}');".format(url))
                self.driver.switch_to.window(self.driver.window_handles[-1]) 
        
        def click_element_with_offset(self, element, xAxis : int, yAxis: int):
                actionChain = ActionChains(self.driver)              
                actionChain.move_to_element_with_offset(element, xAxis, yAxis).click().perform()
                
        def get_news(self):
                jsfile = f"{self.root_app}{os.path.sep}js{os.path.sep}getnews.js"                
                res = self.driver.execute_script(scrpt)     
        
        # loading and refreshing module
        def live_load(self, module_name):
                # live_mod = importlib.import_module(module_name)  
                for mod in sys.modules:
                        del_engine = module_name == mod  # voir in
                if del_engine:
                        del sys.modules[module_name] 
                live_mod = importlib.import_module(module_name)
                importlib.reload(live_mod)
                return live_mod

        def main(self, command="", jsonfile="", param1="", param2=""):                          
                try:          
                        self.trace(inspect.stack())               
                        if command == "":
                                nb_args = len(sys.argv)
                                command = "test" if (nb_args == 1) else sys.argv[1]
                                # fichier json en param
                                jsonfile = "default" if (nb_args < 3) else sys.argv[2].lower()                                
                                param1 = "default" if (nb_args < 4) else sys.argv[3].lower()
                                param2 = "default" if (nb_args < 5) else sys.argv[4].lower()
                                #param3 = "default" if (nb_args < 6) else sys.argv[5].lower()      
                                print("params=", command, jsonfile, param1, param2)                        
                        # debug screen shot
                        # if (command == "conv"):
                        #        img_utils.convert_dir_to_webp(f"{self.root_app}{os.path.sep}data{os.path.sep}results", rm_source=True)
                        #        exit()              
                        
                        humanize = Humanize(self.trace, self.log, self.jsprms.prms['offset_wait'], self.jsprms.prms['wait'], self.jsprms.prms['default_wait'])                       
                        urls = Urls(self.jsprms.prms['urls'])  
                        
                        engine_mod = self.live_load('engine')
                        engine = engine_mod.Engine(self.trace, self.log, self.jsprms, self.dbcontext, self.driver, humanize, self.live_load, urls)                                                
                        
                        if (command == "simplyconnect"):
                                self.driver.get(urls.get_url('base'))
                                wk = input("waiting : ")
                        if (command == "search"):                                                                
                                engine.search()
                                wk = input("waiting 4 : ")
                        if (command == "test"):
                                engine.testit()
                                wk = input("waiting : ")
                        if (command == "reinit_visited"):
                                self.dbcontext.clean_visited()
                        if (command == "get_visited_stats"):
                                visited_stats = self.dbcontext.get_visited_stats()
                                for visited in visited_stats:
                                        print(f"{visited}")
                        if (command == "add_to_keyword"):
                                if (not self.dbcontext.is_in_keyword(param1)):
                                        self.dbcontext.add_to_keyword(param1)
                        if (command == "get_keyword_list"):
                                keywordlist = self.dbcontext.get_keyword_list()
                                self.log.lg("Keyword list")
                                for kw in keywordlist:
                                        print(f"{kw.word}")
                        if (command == "testsc"):
                                self.driver.get(urls.get_url('profile'))
                                while 1==1:                                   
                                        wk = input("wait key 4 screenshot (x to exit) : ")
                                        if wk =="x":
                                                break
                                        today = datetime.now()
                                        dnow = today.strftime(r"%y%m%d%H%M") 
                                        fullfilepath = f"{self.root_app}{os.path.sep}data{os.path.sep}results{os.path.sep}{dnow}.png"
                                        height = self.driver.execute_script("return document.body.scrollHeight")
                                        self.driver.save_screenshot(fullfilepath)
                                        img_utils.convert_to_webp(fullfilepath, 'jpg', rm_source=True)
                        #self.driver.close()
                        ##)  

                        #ONGLETS
                        #driver.switch_to.window(driver.window_handles[-1])       

                except KeyboardInterrupt:
                        print("==Interrupted==")
                        pass
                except Exception as e:
                        print("GLOBAL MAIN EXCEPTION")
                        #self.driver.close()
                        #self.driver.quit()
                        print(f"{inspect.stack()[1].function} {inspect.stack()[1].lineno}")
                        self.log.errlg(e)
                        # raise
                        #
                finally:
                        #self.driver.close()
                        #self.driver.quit()
                
                        print("Finally")                        


              
               
    

        
                

        

