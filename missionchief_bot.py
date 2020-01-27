from splinter import Browser
import time
import platform
import os
from helpers import vehicles,randomint
from colorama import init,Fore,Style
from vehicle import Vehicle
from mission import Mission
init()
operatingsystem = platform.system()
path = os.path.dirname(os.path.realpath(__file__))



class AlreadyExistsException(Exception):
    pass

# Get URL from file
with open(path + "/url.txt", 'r') as f:
    baseurl = f.readline().strip()

class MissonChiefBot:
  def __init__(self):
    self.hrefs= []
    self.missionList = []
    self.vehicleList = []
    logged_in = login(username,password)
    if logged_in:
      while True:
        self.doMissions()
    else: 
      print("Couldn't log in...")
     
  def buildMissions(self):
    print("Building Missions")
    url = baseurl
    hrefs = []
    browser.visit(url)
    links = browser.links.find_by_partial_href('/missions/')
    for link in links:
        hrefs.append(link['href'])
    print(f"{str(len(links))} mission/s found")
    for href in hrefs:
      print(href)
      missionId = href.split("/")[4]
      try:
        for mission in self.missionList:
          if mission.getID == missionId:
            print("ids matched")
            print(mission.getID)
            print(missionId)
            #since the mission is already in the list, we can continue it.
            raise AlreadyExistsException()
        browser.visit(href)
        missionName = browser.find_by_id('missionH1').text          
        requirements = getRequirements(missionId)
        currMission = Mission(missionId,missionName,requirements)
        self.missionList.append(currMission)

      except AlreadyExistsException:
        print("mission except")
        continue
      time.sleep(5)  

  def buildVehicles(self):
    print("Building Vehicles")
    url = baseurl
    hrefs = []
    browser.visit(url)
    links = browser.links.find_by_partial_href('/vehicles/')
    for link in links:
        hrefs.append(link['href'])
    print(f"{str(len(links))} vehicles/s found")
    for href in hrefs:
      vehicleId = href.split("/")[4]
      try:
        for vehicle in self.vehicleList:
          if vehicle.getID == vehicleId:
            #since the vehicle is already in the list, we can continue it.
            raise AlreadyExistsException()
        browser.visit(href)
        vehicleName = browser.find_by_tag('h1').text
        vehicleType = browser.links.find_by_partial_href('/fahrzeugfarbe/').text
        vehicleStatus = browser.find_by_xpath("//span[contains(concat(' ',normalize-space(@class),' '),' building_list_fms')]").text        
        print(f"status {vehicleStatus}")
        currVehicle = Vehicle(vehicleId,vehicleName,vehicleType,vehicleStatus)
        self.vehicleList.append(currVehicle)
      except AlreadyExistsException:
        continue
      time.sleep(5)
      
  def doMissions(self):
    self.buildMissions()
    self.buildVehicles()

    for mission in self.missionList:
        print(mission.getID(),mission.getName(),mission.getStatus())
    for vehicle in self.vehicleList:
        print(vehicle.getID(),vehicle.getName(),vehicle.getStatus(),vehicle.getType()) 
    
    for mission in self.missionList:
      browser.visit("https://www.missionchief.co.uk/missions/"+mission.getID())
      if(mission.getStatus()=="0" or mission.getStatus()==0):
        self.despatchMission(mission)
      elif(mission.getStatus()=="1"):
      # Not all units despatched, need to add addtional 
        pass
      else:
       print(Fore.MAGENTA + f"¬¬¬¬ Mission {mission.getID()} was already despatched, doing nothing..")

    #  Sleep after mission set.
    sleep()
  
  def despatchMission(self,mission):
    print(f"Going to mission {mission.getID()}")
    labels=browser.find_by_css('label[class="mission_vehicle_label"]')
    for requirement in mission.getRequirements():
      todes = int(requirement['qty'])
      des = 0
      checkedunits = False
      try: 
        print(labels.first)
        for label in labels:
            for vehicle in self.vehicleList:
              if(label.text == vehicle.getName() and vehicle.availableDespatch()):
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
                    
    if(checkedunits==True):
      browser.find_by_name('commit').click()	 
      print(f"{des} units despatched")
      # If we have despatched the right amount of units set complete
      if(todes==des):
        mission.setStatus("2")
        # Set to partly despatched
      else:
        mission.setStatus("1")
    Style.RESET_ALL  
      
def sleep():
    rannum = randomint()
    print(Fore.CYAN + f"Sleeping for {str(rannum)} seconds")
    Style.RESET_ALL
    time.sleep(rannum)
   
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
 MissonChiefBot()

if __name__ == '__main__':
 begin()