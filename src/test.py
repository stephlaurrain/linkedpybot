import os
from os import path
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# initialisation du driver chrome
options = webdriver.ChromeOptions()
# où va se situer le profile chrome spécifique au projet
# ce n'est pas obligatoire d'en avoir un, mais c'est utile dans le cas où l'on veut conserver historique ou connexion, installer des extensions spécifiques
options.add_argument("user-data-dir=./chromeprofile")
# anti bot detection : empêche le site distant de detecteur que c'est une instance chrome de Selenium qui interagit
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# démarrer avec le navigateur en taille maximale (ça peut aider quand la detection d'éléments ne fonctionne pas)
options.add_argument("--start-maximized")
# affiche les images (on pourrait s'en passer)
prefs = {"profile.managed_default_content_settings.images": 1}
options.add_experimental_option("prefs", prefs)
# instancie le driver chrome avec les options définies ci-dessus
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# autre option anti detection de robot
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# maximiser l'affichage encore une fois
driver.maximize_window()
# définir le temps que mettra le driver pour chercher des éléments
driver.implicitly_wait(10)


# ouvrir le site "openclassrooms"
driver.get("http://www.openclassrooms.fr")
input("press key")

# fonction pour cliquer sur le lien pour refuser les cookies
def click_cookie():
    # on va chercher l'élément dans la page
    # exemple de "selector" : #truste-consent-required
    # exemple de xpath : //*[@id="truste-consent-required"]
    # exemple de full xpath : /html/body/div[8]/div/div[2]/div[3]/div[2]/button[1]
    element = driver.find_element(By.ID, 'truste-consent-required')
    input("press a key")
    # on click sur l'élément
    element.click()
    input("press key")


# click_cookie()

def search():
    #main-search > div > form > button.webapp-0-webapp95.webapp-0-webapp97

    # //*[@id="main-search"]/div/form/b   
    #el_main_search = driver.find_element(By.ID, 'main-search')
    # attention : recherche à partir de el_main_search
    # el_form = el_main_search.find_element(By.TAG_NAME, 'form')
    # input("press k")
    
    # driver.execute_script("document.getElementById('algolia-search-input').style.with = '200px';")
    search_zone = driver.find_element(By.ID, 'algolia-search-input')    
    driver.execute_script("document.getElementById('algolia-search-input').value = 'TEST';")
    # search_zone.send_keys("Hello, World!")    
    # driver.execute_script("alert('test');")
    # search_zone.send_keys("Hello, World!")  
    input("press k")
    

# execution de la fonction de recherche de l'exemple
search()


# extension contre cookies = I don't care about cookies