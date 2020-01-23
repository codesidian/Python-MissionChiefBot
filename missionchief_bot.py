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
      rannum = randomint()
      print(Fore.CYAN + f"Sleeping for {str(rannum)} seconds")
      Style.RESET_ALL
      time.sleep(rannum)
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
        print(f"{str(len(links))} missions found")
        for link in links: 
         hrefs.append(link['href'])
        doMissions()
    except:
        time.sleep(1)

def getRequirements(missionId):
  requirementsurl = baseurl + "/einsaetze/3?mission_id=" + missionId
  browser.visit(requirementsurl)
  requiredlist = []
  requirements = browser.find_by_tag('td')
  Style.RESET_ALL
  print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  for index, r in enumerate(requirements):
    if "Required" in r.text:
     if "Station" not in r.text:
      requirement = r.text.replace('Required','').strip();
      qty = requirements[index+1].text
      print(f"Requirement found :   {str(qty)} x {str(requirement)}")
      requiredlist.append({'requirement':requirement,'qty': qty })
  print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  Style.RESET_ALL
  return requiredlist
    
def doMissions():
 count = 0
 for href in hrefs:
  count+=1  
  try:
   browser.visit(href)
   mission_str = str(count)
   mission_text = browser.find_by_id('missionH1').text
   print("MISSION " + mission_str +": " + mission_text)
   missionId = href.split("/")[4]
   for miss in despatched:
     if(miss==missionId):
       print(f"Already despatched this mission {missionId} - Skipping it")
       rannum = randomint()
       print(Fore.CYAN + f"Sleeping for  {rannum} - seconds")
       Style.RESET_ALL
       time.sleep(rannum)
       continue
   Style.RESET_ALL
   print(Fore.CYAN + "Getting requirements")
   requiredlist=getRequirements(missionId)
   print(Fore.CYAN + "Got Requirements")
   Style.RESET_ALL
   browser.visit(href)
   labels=browser.find_by_css('label[class="mission_vehicle_label"]')

   for requirement in requiredlist:
    try:
      # Here we are seeing is any labels exists (i.e do we even have any vehicles we can despatch- if we don't throw print the below.)
     print(labels.first);
    except:
      print(Fore.RED + "MISSION " + mission_str +":" + "CAN NOT DESPATCH A UNIT, ALL IN USE OR UNIT ALREADY DESPATCHED")
      Style.RESET_ALL
    for label in labels:
      if(requirement['requirement'] in label.text):
       print("Direct match found...")
       checkid = label['id'].split("_")[3]
       checkbox=browser.find_by_css('input[class="vehicle_checkbox"]')
       for check in checkbox:
        if(check['value'] == checkid):
         check.check()
      else:
       print("Couldn't find a direct match...")
       print("Checking keywords..")
       for category in vehicles:
        for i in range(int(requirement['qty'])):
         for vehicle in vehicles[category]:
           print(f"Checking {vehicle} against {label.text}")
           if(vehicle in label.text):
            checkid = label['id'].split("_")[3] 
            checkbox=browser.find_by_css('input[class="vehicle_checkbox"]')
            for check in checkbox:
                if(check['value']==checkid):
                    if(check['value']==checkid):
                      print(Fore.GREEN + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                      print(Fore.GREEN + f"Attempting to despatch {label.text}")
                      check.check()
                      print(Fore.GREEN + f"{label.text} despatched!")
                      print( Fore.GREEN +"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                      despatched.append(missionId)
            browser.find_by_name('commit').click()
            Style.RESET_ALL
           else:
            print(Fore.RED + "All the vehicles are out that we need")
            Style.RESET_ALL

        Style.RESET_ALL

  except Exception as e:
   print(Fore.RED + "MISSION " + mission_str +":" + "CAN NOT DESPATCH A UNIT, ALL IN USE OR UNIT ALREADY DESPATCHED")
   Style.RESET_ALL

    
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