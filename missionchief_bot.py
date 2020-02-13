from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
import time
import platform
import os
from helpers import vehicles,randomint
from colorama import init,Fore,Style
from vehicle import Vehicle
from mission import Mission
from despatch import Despatch
import logging
import configparser
init()


#Skip doing missions, just build data. (for testing)
JUST_BUILD_DATA = False


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

class AlreadyExistsException(Exception):
    pass
class NothingToDespatch(Exception):
    pass

class MissonChiefBot:
  def __init__(self):
    self.hrefs= []
    self.missionList = []
    self.vehicleList = []
    self.despatches = []
    self.missionsSeen = []
    
    logger.info("Attempting login")
    logged_in = login(username,password)
    if logged_in:
      logger.info("User is logged in")
      logger.info("Building Vehicles")
      self.buildVehicles()
      while True:
        try:
          logger.info("Doing missions")
          self.doMissions()
        except Exception as e:
          logger.error("An error occurred, program exiting.")
          logger.error(e)
          print(Fore.RED + "Oh no, an error occurred." +Style.RESET_ALL)
          print(e)
          print(Fore.RED + "Please create an issue on github or post in our discord\n"+
                "Include your output and the debug.log file so we can debug it! :)" +Style.RESET_ALL)
          
          break
    else: 
      print("Couldn't log in...")
     
  def buildMissions(self):
    """
      Build a list of current missions and remove completed
    """
    print("Removing Completed")
    #Check and remove completed missions
    logger.debug("Removing completed missions")
    oldMissions = self.missionList
    compNum = 0
    haveVehiclesAvailable = False
    hrefs = []
    url = BASE_URL
    for oldMission in oldMissions:
      browser.get(BASE_URL + "missions/"+oldMission.getID())
      try:
        compNum = compNum + 1
        if browser.find_element_by_class_name('missionNotFound'):
          logger.debug("%s wasn't found. Treating it as complete and removing.",oldMission.getID())
          print(Fore.GREEN + oldMission.getName() + " was completed." +Style.RESET_ALL)
          self.missionList.remove(oldMission)
          for d in self.despatches:
            if d.getID() == oldMission.getID():
              for dv in d.getVehicles():  
                for v in self.vehicleList:
                  if dv == v.getID():
                    v.setStatus('1')
          tempMissionSeen = self.missionsSeen
          for h in tempMissionSeen:
            if oldMission.getID() in h:
              self.missionsSeen.remove(h) 
          self.despatches.remove(oldMission)
          
      except NoSuchElementException:
        continue
    logger.debug("%s missions completed",compNum)
    logger.debug("Building missions list")
    print("Building New Missions")
    logger.debug("Grabbing mission urls and hrefs")
    browser.get(url)
    links = browser.find_elements_by_xpath("//a[contains(@href,'missions')]")
    checked = 0
    currBatchNum = 0
    for link in links:
        hrefs.append(link.get_attribute('href'))
    print(f"{str(len(links))} mission/s found")
    logger.debug("Building info for %s missions", len(hrefs))
    for v in self.vehicleList:
      if v.despatchable():
        haveVehiclesAvailable = True
        break
      
    if haveVehiclesAvailable:
      for href in hrefs:
        missionId = href.split("/")[4]
        if(href not in self.missionsSeen and currBatchNum < MISSION_BATCH_NUM):
          currBatchNum+=1
          self.missionsSeen.append(href)
          try:
            for mission in self.missionList:
              if mission.getID() == missionId:
                #since the mission is already in the list, we can continue it.
                raise AlreadyExistsException()
            logger.debug("%i/%i missions checked against batch amount",currBatchNum,MISSION_BATCH_NUM)
            logger.debug("Getting vehicle info for %s", missionId)
            browser.get(BASE_URL + "missions/"+missionId)
            missionName = browser.find_element_by_id('missionH1').text   
            logger.debug("Mission name is %s", missionName)    
            logger.debug("Getting requirements for %s",missionId)   
            requirements = getRequirements(missionId)
            logger.debug("Mission requirements are %s", requirements)
            currMission = Mission(missionId,missionName,requirements)
            logger.debug("Mission info built, adding to list")
            self.missionList.append(currMission)
            # Show user how many missions it's checked compared to how many it needs to.
            checked+=1
            print(Fore.GREEN + f"{checked}/{MISSION_BATCH_NUM} missions checked!" + Fore.RESET)
          except AlreadyExistsException:
            continue
        logger.debug("%s/%s missions built",checked,len(hrefs))
    else:
      logging.debug("No vehicles available, not checking missions")


  def buildVehicles(self):
    """
      Build a list of the user's vehicles
    """
    print("Building Vehicles") 
    hrefs = []
    logger.debug("Grabbing vehicle urls and hrefs")
    browser.get(BASE_URL + "vehicles")
    links = browser.find_elements_by_xpath("//a[contains(@href,'vehicles')]")
    for link in links:
        hrefs.append(link.get_attribute("href"))
    print(f"{str(len(links))} vehicles/s found")
    checked = 0
    logger.debug("Building info for %s vehicles", len(hrefs))
    for href in hrefs:
      vehicleId = href.split("/")[4]
      try:
        for vehicle in self.vehicleList:
          if vehicle.getID == vehicleId:
            #since the vehicle is already in the list, we can continue it.
            raise AlreadyExistsException()
        logger.debug("Getting vehicle info for %s", vehicleId)
        browser.get(BASE_URL + "vehicles/"+vehicleId)
        vehicleName = browser.find_element_by_tag_name('h1').text
        logger.debug("Vehicle name is %s", vehicleName)
        vehicleType = browser.find_element_by_xpath("//a[contains(@href,'fahrzeugfarbe')]").text
        logger.debug("Vehicle type is %s", vehicleType)
        vehicleStatus = browser.find_element_by_xpath('//span[contains(@class, "building_list_fms")]').text
        logger.debug("Vehicle type is %s", vehicleStatus)
        currVehicle = Vehicle(vehicleId,vehicleName,vehicleType,vehicleStatus)
        logger.debug("Vehicle info built, adding to list")
        self.vehicleList.append(currVehicle)
        checked+=1
        print(Fore.GREEN + f"{checked}/{len(hrefs)} vehicles checked!" + Fore.RESET)
      except AlreadyExistsException:
        continue
    logger.debug("%s/%s vehicles built",checked,len(hrefs))

      
  def doMissions(self):
    """
      Rebuild the mission list, check for partial despatches and despatch. 
    """
    logger.info("Building missions")
    self.buildMissions()
    print(Fore.MAGENTA + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
    print(Fore.MAGENTA +"Your Missions"+Style.RESET_ALL)
    for mission in self.missionList:
        print("Name: " + mission.getName())
    print(Fore.MAGENTA +"Your Vehicles"+Style.RESET_ALL)
    for vehicle in self.vehicleList:
        print("Name: "+ vehicle.getName()+ " | Type: " +vehicle.getType()) 
    print(Fore.MAGENTA + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
    if not JUST_BUILD_DATA:
      print("Doing missions")
      logger.info("Doing missions")
      for mission in self.missionList:
        print("Checking if "+ mission.getName()+" has units responding")
        logger.debug("Checking if %s has already been dispatched", mission.getName())
        if(mission not in self.despatches):
          logger.debug("It hasn't, despatching.")
          self.despatchVehicles(mission)
        else:
          logger.debug("Checking if %s is partial despatch", mission.getName())
          #We need to make sure that there's no missions with half dispatches (if there weren't enough vehicles to begin with)
          for despatch in self.despatches:
            if despatch == mission:
              totalVehiclesRequired = 0
              for requirement in mission.getRequirements():
                totalVehiclesRequired += int(requirement['qty'])
              if totalVehiclesRequired > len(despatch.getVehicles()):
                #If the amount of despatched vehicles is less than required. We can retry the dispatch
                logger.debug("%s/%s have been dispatched, dispatching more",len(despatch.getVehicles()),totalVehiclesRequired)
                print(mission.getName() + " still needs vehicles. Despatching...")
                self.despatchVehicles(mission)
              else:
                logger.debug("%s/%s have been dispatched, moving on.",len(despatch.getVehicles()),totalVehiclesRequired)
                
          print(f"Mission {mission.getName()} was already despatched, doing nothing..")
    else:
      print("Not doing missions. Debug build only. ")
      logger.warning("Bot in build only mode. Not doing missions.")
          
    #  Sleep after mission set.
    sleep()

  def despatchVehicles(self,mission):
    """
      Despatch vehicles based on the passed mission's requirements \n
      Mission (MissionObj): The mission to be despatched
    """
    logger.info("Dispatching vehicles to %s",mission.getName())
    print(f"Going to mission {mission.getName()}")
    logger.debug("Visiting the url")
    browser.get(BASE_URL + "missions/"+mission.getID())
    print("Checking requirements for " + mission.getName())
    despatchedVehicles = []
    logger.debug("Going through the requirements")
    for requirement in mission.getRequirements():
      todes = int(requirement['qty'])
      logger.debug("%s %s are needed",todes,requirement['requirement'])
      des = 0
      checkedunits = False
      logger.debug("Going through the requirements and the user's vehicles to dispatch")
      try: 
        for category in vehicles:
          #Only need to check for required types
          if requirement['requirement'] == category:
            print("Mission needs "+str(todes)+" " + category)
            for vehicle in vehicles[category]:
              for ownedVehicle in self.vehicleList:
                if(ownedVehicle.getType() == vehicle and (ownedVehicle.despatchable())):
                  logger.debug("User has %s %s available",ownedVehicle.getType(),category)
                  #print("We have a " + category + " " + ownedVehicle.getType() + " available")
                  #vehicleStatus = browser.find_element_by_xpath('//span[contains(@class, "building_list_fms")]').text  
                  
                  # If amount of despatched is less than required.
                  logger.debug("Checking if there required quantity as been achieved")  
                  if(des<todes):
                    logger.debug("Mission still needs vehicles, despatching.")
                    print("Despatching " + ownedVehicle.getName() + " to " + mission.getName())
                    try:
                      logger.debug("Finding vehicle's checkbox")  
                      checkbox = browser.find_element_by_xpath('//input[contains(@id, '+ownedVehicle.getID() +')]')                
                      # Scroll the element
                      browser.execute_script("arguments[0].scrollIntoView();", checkbox)
                      checkbox.click()
                      checkedunits = True     
                      des+=1
                      logger.debug("Adding vehicle to despatched list, and setting it as despatched")
                      despatchedVehicles.append(ownedVehicle.getID())   
                      ownedVehicle.setDespatched()       
                    except (NoSuchElementException) as e: 
                      logger.error("Vehicle checkbox cannot be found, or clicked" + ownedVehicle.getID())
                      continue
             
            #we can skip the next categories as this requirement has now been fulfilled
            break
      except NothingToDespatch as e:
        logger.error("There's nothing to despatch: %s",e)
        continue            
    # If units have been checked, we need to despatch them.
    logger.debug("Checking if there are vehicles checked")
    if(checkedunits==True):
      logger.debug("Submitting mission")
      browser.find_element_by_name('commit').click()
      print(f"{des} units despatched")
      logger.debug("%s vehicles have been despatched", des)
      ########################################
      # ### Example of getting vehicle arrival time, might be useful information to grab.
      # if ownedVehicle.getStatus() == '3':
      #   # We sleep as it's not immediately available
      #   time.sleep(5)
      #   try:
      #     remaining = browser.find_element_by_id('vehicle_drive_'+ ownedVehicle.getID()).text
      #     browser.execute_script("arguments[0].scrollIntoView();", remaining)
      #     print(f"{ownedVehicle.getName()} - {remaining} time remaining till arrival")
      #   except NoSuchElementException as e: 
      #     logger.debug("Could not find remaining time element")
      # ########################################
      logger.debug("Checking if missions is in our despatches")
      if(mission not in self.despatches):
        logger.debug("Adding it")
        currDespatch = Despatch(mission.getID(),despatchedVehicles,10)
        self.despatches.append(currDespatch)
      else:
        logger.debug("Already exists, fulfilled partial despatch")
    else:
      logger.debug("No vehicles select, nothing to despatch")
      print("Nothing to despatch")
      
  def logState(self):
    """
      Output program state to the logfile
    """
    #TODO: Append vehicle list, mission list and despatches state to the log file.
    with open("debug.log", "a") as log:
      log.write("")
      
def sleep():
    print(Fore.CYAN + f"Sleeping for {str(15)} seconds"+Style.RESET_ALL)
    time.sleep(15)
   
def login(username,password):
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
    try : 
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


def getRequirements(missionId):
  """
    Returns a list of requirements given a missionId\n
    missionId (str): An ID of a mission
  """
  logger.debug("Grabbing requirements for %s",missionId)
  print("Getting requirements")
  
  requirementsurl = browser.find_element_by_xpath('//a[contains(@href, "einsaetze")]').get_attribute('href')
  logger.debug("Visiting %s",requirementsurl)
  browser.get(requirementsurl)
  requiredlist = []
  logger.debug("Grabbing table elements")
  requirements = browser.find_elements_by_tag_name('td')
  print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
  logger.debug("Looping through the table to extract each vehicle")
  for index, r in enumerate(requirements):
    if r.text:
     if "Required" in r.text:
      if "Station" not in r.text:
       requirement = r.text.replace('Required','').strip().lower()
       qty = requirements[index+1].text
       print(f"Requirement found :   {str(qty)} x {str(requirement)}")
       requiredlist.append({'requirement':requirement,'qty': qty })
  print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
  logger.warning("No requirements were found, appending 1 ambulance?")
  if(len(requiredlist)==0):
   requiredlist.append({'requirement':'ambulance','qty': 1 })

  return requiredlist


logger = setup_logger('botLogger','debug.log',level=logging.DEBUG)
operatingsystem = platform.system()
path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read('config.ini')
BASE_URL = config['DEFAULT']['url']
MISSION_BATCH_NUM = int(config['DEFAULT']['mission_batch_amount'])
username = config['DEFAULT']['email'].strip()
password = config['DEFAULT']['password'].strip()

if not os.path.exists("chromedriver.exe"):
  print("Please make sure chromedriver.exe is in the project folder."+
        "\nGet the correct one for your version of chrome here:"+
        "\nhttps://chromedriver.chromium.org/downloads")
  raise SystemExit

browser = webdriver.Chrome()

def begin(): 
 MissonChiefBot()

if __name__ == '__main__':
 begin()
 
