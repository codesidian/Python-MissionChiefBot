
import platform,os,sys,logging,configparser,json,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

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
    if(os.path.exists(jsonpath) == False):
      os.mkdir(jsonpath)
    with open(jsonpath + missionId +'.json', 'w') as outfile:
      data  = {}
      data['missionId'] = missionId
      data['missionName'] = missionName
      data['requirements'] = requirements
      json.dump(data, outfile)

# Grabs the requirements
def getRequirements():
  requirements = browser.find_elements_by_tag_name('td')
  requiredlist = []
  for index, r in enumerate(requirements):
    if r.text:
     if "Required" in r.text or "Требуемые" in r.text or "Benodigde" in r.text or "benodigd" in r.text or "Nödvändiga" in r.text or "richieste" in r.text or "richiesta" in r.text or "richiesti" in r.text or "Benötigte" in r.text:
      if "Station" not in r.text and "Caserme" not in r.text and "Stazioni" not in r.text and "Possibilità" not in r.text and "Possibile" not in r.text and "brandstationer" not in r.text and "räddningstationer" not in r.text:
       requirement = r.text.replace('Required','').replace('Требуемые','').replace("Benodigde",'').replace("benodigd",'').replace("Nödvändiga","").replace("richieste","").replace("richiesti","").replace("richiesta","").replace("Benötigte","").strip().lower()
       qty = requirements[index+1].text
       print(f"Requirement found :   {str(qty)} x {str(requirement)}")
       requiredlist.append({'requirement':requirement,'qty': qty })
  if(len(requiredlist)==0):
   requiredlist.append({'requirement':'ambulance','qty': 1 })
  return requiredlist

config = configparser.ConfigParser()
config.read('../config.ini')
SERVER = config['DEFAULT']['server']

servers = configparser.ConfigParser()
servers.read('../server.ini')
BASE_URL = servers[SERVER]['url']
SERVER_REGION = servers[SERVER]['name']


# Check and install chrome driver to path depending on the os.
chromedriver_autoinstaller.install() 

chrome_options = Options()  
if config['DEFAULT'].getboolean('headless_mode') == True:
  chrome_options.add_argument("--headless")  
browser = webdriver.Chrome(options=chrome_options)



getMissions()