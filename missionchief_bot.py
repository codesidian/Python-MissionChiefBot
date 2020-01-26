from splinter import Browser
import time
import platform
import os
from helpers import vehicles,randomint
from colorama import init,Fore,Style
init()
operatingsystem = platform.system()
hrefs= []
path = os.path.dirname(os.path.realpath(__file__))
despatched = []
checkedrecently= []
# Get URL from file
with open(path + "/url.txt", 'r') as f:
    baseurl = f.readline().strip()

class MissonChiefBot:
 def init(self):
    logged_in = login(username,password)
    if logged_in:
     while True:
      hrefs.clear()
      getMissions()
    else: 
     print("Couldn't log in...")

def login(username,password):
    print(Fore.CYAN + "Logging in")
    Style.RESET_ALL
    # Visit URL
    url = baseurl+"/users/sign_in"
    browser.visit(url)
    # Filling in login information
    browser.fill("user[email]",username)
    browser.fill("user[password]",password)
    # Submitting login
    browser.find_by_name('commit').click()
    try : 
     # check we are logged in- by grabbing a random tag only visible on log in.
     alliance = browser.find_by_id('alliance_li')
     print("Logged in")
     if alliance['class']=="dropdown":
      return True
     else:
      return False
    except Exception: 
     return False

def getMissions():
    print(Fore.CYAN + "Getting missions")
    url = baseurl
    browser.visit(url)
    # Finding links for missions
    try:
        links = browser.links.find_by_partial_href('/missions/')
        print(f"{str(len(links))} mission/s found")
        for link in links: 
         hrefs.append(link['href'])
        doMissions()
    except:
        time.sleep(1)

def getRequirements(missionId):
  print("Getting requirements")
  requirementsurl = browser.links.find_by_partial_href('/einsaetze/')[0]['href']
  browser.visit(requirementsurl)
  requiredlist = []
  requirements = browser.find_by_tag('td')
  Style.RESET_ALL
  print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  Style.RESET_ALL
  for index, r in enumerate(requirements):
    if r.text:
     if "Required" in r.text:
      if "Station" not in r.text:
       requirement = r.text.replace('Required','').strip().lower();
       qty = requirements[index+1].text
       print(f"Requirement found :   {str(qty)} x {str(requirement)}")
       requiredlist.append({'requirement':requirement,'qty': qty })
  print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  Style.RESET_ALL
  if(len(requiredlist)==0):
   requiredlist.append({'requirement':'ambulance','qty': 1 })
  return requiredlist
    
def doMissions():
 count = 0
 for href in hrefs:
  count+=1  
  browser.visit(href)
  mission_str = str(count)
  mission_text = browser.find_by_id('missionH1').text
  print(Fore.MAGENTA + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  Style.RESET_ALL
  print("MISSION " + mission_str +": " + mission_text)
  missionId = href.split("/")[4]
  
  if(len(despatched)==0):
    doMission(href,missionId)

  else:
    for mission in despatched:
      if(mission==missionId):
        print(Fore.MAGENTA + f"¬¬¬¬ Mission {missionId} was already despatched, doing nothing..")
      else:
        doMission(href,missionId)
#  Sleep after mission set.
 rannum = randomint()
 print(Fore.CYAN + f"Sleeping for {str(rannum)} seconds")
 Style.RESET_ALL
 time.sleep(rannum)      
  

def doMission(href,missionId):
    requirements = getRequirements(missionId);
    print("Got Requirements")
  
    print(f"Going to mission {missionId}")
    browser.visit(href);
    labels=browser.find_by_css('label[class="mission_vehicle_label"]')
    for requirement in requirements:
      todes = int(requirement['qty'])
      des = 0
      checkedunits = False
      try: 
        print(labels.first)
        for label in labels:
          for category in vehicles:
            for vehicle in vehicles[category]:
              if(label.text == vehicle):
                checkid = label['id'].split("_")[3] 
                checkbox=browser.find_by_css('input[class="vehicle_checkbox"]')
                for check in checkbox:
                  if(check['value']==checkid):
                                      
                    if(des<todes):
                      print(Fore.GREEN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")              
                      print(Fore.GREEN + f"Attempting to check {label.text}")
                      check.check()
                      checkedunits = True
                      print(Fore.GREEN + f"{label.text} checked!")	             
                      des+=1                       
                      print( Fore.GREEN +"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    Style.RESET_ALL
      except Exception as e:
        print("Nothing to despatch");           
        continue
    browser.find_by_name('commit').click()	                       
    print(f"{des} units despatched")
    if(checkedunits==True):
      if(missionId not in despatched):
        despatched.append(missionId)
    Style.RESET_ALL
    return True
  
      

# Taking account information from file
with open(path + '/account.txt', 'r') as f:
    username = f.readline().strip()
    password = f.readline().strip()
    

# Setting up browser
if operatingsystem == "Windows":
 executable_path = {'executable_path': path +'/chromedriver.exe'}
elif operatingsystem == "Linux":
  executable_path = {'executable_path': path +'/linux/chromedriver'}

elif operatingsystem == "Darwin":
  executable_path = {'executable_path': path+'/mac/chromedriver'}
 
browser = Browser('chrome', **executable_path)

def begin(): 
 MissonChiefBot().init()

if __name__ == '__main__':
 begin()