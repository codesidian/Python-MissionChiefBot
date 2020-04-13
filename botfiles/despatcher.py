"""
Despatcher for MissionChief Bot, made for transporting vehicles.
Creative Commons Attribution-NonCommercial 4.0 International License
Author - Jack Bayliss 10/04/2020
"""
import platform, os, sys, logging, configparser, json, time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from colorama import init,Fore,Style

class MissionChiefDespatcher():
 def __init__(self):
  init()
  self.handleDespatch()
 def pageloaded(self): 
   WebDriverWait(browser, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
   return True
 def handleDespatch(self):
     logged_in = login(username,password,browser)
     if logged_in: 
      while True:
       browser.get(BASE_URL)
       if self.pageloaded():
        try:
          transports = browser.find_elements_by_xpath("//ul[contains(@id,'radio_messages_important')]/li[not(contains(@style,'display:none'))]/span[contains(@class,'building_list_fms_5')]/following-sibling::a[contains(@href,'missions')]")
        except (NoSuchElementException,ElementClickInterceptedException):
          print("Nothing found that needs transporting.. sleeping")
          time.sleep(120)
        
        
       hrefs = []
       # We push them into a new list so it doesnt cause issues with selenium.
       for transport in transports:
        hrefs.append(transport.get_attribute('href'))
        
       for href in hrefs:
        browser.get(href)
        if self.pageloaded():
          transport = browser.find_elements_by_id("process_talking_wish_btn")
          threfs = []
          for t in transport:
            # We again push them to a new href list, so that we dont get a stale element.
            threfs.append(t.get_attribute('href'))
          for thref in threfs:
            browser.get(thref)
            transportbtn = browser.find_elements_by_xpath('//a[contains(@href, "patient")][contains(@class,"btn-success")]')[0]
            browser.execute_script("arguments[0].scrollIntoView();", transportbtn)
            transportbtn.click()
            browser.back()
       print("Transported all found sleeping")
       time.sleep(120)
     else:
      print("Login failed")
      
  
def login(username,password,browser):
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
    print("Connecting to the region: ", SERVER_REGION ) 
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)

    print(Fore.CYAN + "logging in"+Style.RESET_ALL)
    # Visit URL
    url = BASE_URL+"/users/sign_in"
    logger.info("Visiting %s",url)
    browser.get(url)
    
    # Filling in login information
    user =  browser.find_element_by_id('user_email')
    passw = browser.find_element_by_id('user_password')
    user.send_keys(username)
    passw.send_keys(password)
    # Submitting login
    logger.info("Submitting login form")
    browser.find_element_by_name('commit').click()
    try: 
     # check we are logged in- by grabbing a random tag only visible on log in.
     logger.debug("Checking if logged in")
     alliance = browser.find_element_by_id('alliance_li')
     if alliance.get_attribute('class')=="dropdown":
      logger.debug("Element found, user is logged in")
      print("Logged in")
      return True
     else:
      logger.debug("Element not found, user is not logged in")
      return False
    except Exception as e: 
     logger.error("Grabbing element failed err: %s",e)
     return False  

config = configparser.ConfigParser()
config.read('../config/config.ini')
SERVER = config['DEFAULT']['server']
MISSION_BATCH_NUM = int(config['DEFAULT']['mission_batch_amount'])
username = config['DEFAULT']['email'].strip()
password = config['DEFAULT']['password'].strip()

servers = configparser.ConfigParser()
servers.read('../config/server.ini')
BASE_URL = servers[SERVER]['url']
SERVER_REGION = servers[SERVER]['name']

def setup_logger(name, logFile, level=logging.INFO):
  """Returns a ready to go logger\n
    name (str): Desired name of the logger\n
    logFile (str): Desired filename to be logged to\n
    level (logging.LEVEL): Level of logging on the logger
  """
  fHandler = logging.FileHandler(logFile)   
  formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(funcName)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')     
  fHandler.setFormatter(formatter)
  logger = logging.getLogger(name)
  logger.setLevel(level)
  logger.addHandler(fHandler)
  return logger

logger = setup_logger('botLogger','debug.log',level=logging.CRITICAL)

# Check and install chrome driver to path depending on the os.
chromedriver_autoinstaller.install() 

chrome_options = Options()  
chrome_options.add_argument("--start-maximized");

if config['DEFAULT'].getboolean('headless_mode'):
  chrome_options.add_argument("--headless")  

if "pytest" in sys.modules:
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
browser = webdriver.Chrome(options=chrome_options)



try:
 MissionChiefDespatcher()
except KeyboardInterrupt:
 print('Closing..')
 logger.debug("Closing despatcher.")
 try:
  sys.exit(1)
 except SystemExit:
  os._exit(1)
