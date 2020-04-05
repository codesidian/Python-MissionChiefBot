
import platform, os, sys, logging, configparser, json, time, chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Grabs all the missions we can find, and generates a .JSON file for each one.
def getMissions():
 hrefs = []
 browser.get(BASE_URL + "/einsaetze");
 links = browser.find_elements_by_xpath("//a[contains(@href,'einsaetze')]")
 for link in links:
    hrefs.append(link.get_attribute('href'))
  
 for href in hrefs:
    missionId = href.split('/')[4]
    browser.get(href)
    missionName = browser.find_element_by_tag_name('h1').text
    requirements = getRequirements()
    jsonpath = '../json/missions/' + SERVER  + '/'
    if not os.path.exists(jsonpath):
      os.mkdir(jsonpath)
    with open(jsonpath + missionId +'.json',"w+",encoding="utf8") as outfile:
      data  = {}
      data['missionId'] = missionId
      data['missionName'] = missionName
      data['requirements'] = requirements
      json.dump(data, outfile)

# Grabs the requirements
def getRequirements():
  requirements = browser.find_elements_by_tag_name('table')[1].find_elements_by_tag_name('td')
  requiredlist = []
  for index, r in enumerate(requirements):
    if not r.text.isdigit() and len(r.text)>0:
        requirement = r.text.replace('Required','').replace('Wymagane','').replace('Wymagany','').replace('Требуемые','').replace("Benodigde",'').replace("benodigd",'').replace("Nödvändiga","").replace("richieste","").replace("richiesti","").replace("richiesta","").replace("Benötigte","").strip().lower()
        qty = requirements[index+1].text
        print(f"Requirement found : {str(qty)} x {str(requirement)}")
        requiredlist.append({'requirement':requirement,'qty': qty })
  if len(requiredlist)==0:
   requiredlist.append({'requirement':'ambulance','qty': 1 })
  return requiredlist

config = configparser.ConfigParser()
config.read('../config/config.ini')
SERVER = config['DEFAULT']['server']

servers = configparser.ConfigParser()
servers.read('../config/server.ini')
BASE_URL = servers[SERVER]['url']
SERVER_REGION = servers[SERVER]['name']


# Check and install chrome driver to path depending on the os.
chromedriver_autoinstaller.install() 

chrome_options = Options()  
if config['DEFAULT'].getboolean('headless_mode'):
  chrome_options.add_argument("--headless")  
browser = webdriver.Chrome(options=chrome_options)



getMissions()
