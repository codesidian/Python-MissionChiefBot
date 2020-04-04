from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import platform,os,sys,logging,configparser,json,time
from helpers import randomsleep
from colorama import init,Fore,Style
from vehicle import Vehicle
from mission import Mission
from despatch import Despatch
import chromedriver_autoinstaller



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
          print(Fore.RED + "Restarting bot...." +Style.RESET_ALL);
    else: 
      print("Couldn't log in...")
  def pageloaded(self): 
   browser.execute_script('return document.readyState;')
   return True


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
        if browser.find_element_by_xpath("//div[contains(@class,'missionNotFound')]"):
          logger.debug("%s wasn't found. Treating it as complete and removing.",oldMission.getID())
          print(Fore.GREEN + oldMission.getName() + " was completed." +Style.RESET_ALL)
          try:
           self.missionList.remove(oldMission)
          except Exception as e:
           logger.debug("Caught .remove error, continuing.")
           continue
          for d in self.despatches:
            if d.getID() == oldMission.getID():
              for dv in d.getVehicles():  
                for v in self.vehicleList:
                  if dv == v.getID():
                    v.setStatus('1')
          tempMissionSeen = self.missionsSeen

          try:
            for h in tempMissionSeen:
              if oldMission.getID() in h:
                self.missionsSeen.remove(h) 
            self.despatches.remove(oldMission)
          except Exception as e:
           logger.debug("Caught .remove error, continuing.")
           continue
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
            with open('../json/missions.json') as missions_json:
              mdata = json.load(missions_json)
              if missionId in mdata['missions']: 
                logger.debug("Mission exists in JSON file")
                mission = mdata['missions'][missionId]
                requirements = json.loads(mission['requirements'])
                currMission = Mission(missionId,mission['missionName'],requirements)
              else:
               logger.debug("Mission does not exists in JSON file")
               logger.debug("%i/%i missions checked against batch amount",currBatchNum,MISSION_BATCH_NUM)
               logger.debug("Getting vehicle info for %s", missionId)
               browser.get(BASE_URL + "missions/"+missionId)
               try:
                missionName = browser.find_element_by_id('missionH1').text 
               except Exception as e:
                continue
               logger.debug("Mission name is %s", missionName)    
               logger.debug("Getting requirements for %s",missionId)   
               requirements = getRequirements(missionId)
               logger.debug("Mission requirements are %s", requirements)
               currMission = Mission(missionId,missionName,requirements)
               with open('../json/missions.json', 'w') as outfile:
                  logger.debug("Buidling mission JSON object")
                  mdata['missions'][missionId] = {}
                  mdata['missions'][missionId]['missionName'] = missionName
                  mdata['missions'][missionId]['requirements'] = json.dumps(requirements,indent=4)
                  logger.debug("Adding mission to JSON file")
                  json.dump(mdata,outfile,sort_keys=True,indent=4)

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
        with open('../json/vehicles.json') as vehicles_json:
          vdata = json.load(vehicles_json)
          if vehicleId in vdata['vehicles']: 
           logger.debug("Vehicle exists in JSON file")
           veh = vdata['vehicles'][vehicleId]
           currVehicle = Vehicle(vehicleId,veh['vehicleName'],veh['vehicleType'],veh['vehicleStatus'])
          else:
            logger.debug("Vehicle does not exist in JSON file")
            logger.debug("Getting vehicle info for %s", vehicleId)
            browser.get(BASE_URL + "vehicles/"+vehicleId)
            vehicleName = browser.find_element_by_tag_name('h1').text.lower()
            logger.debug("Vehicle name is %s", vehicleName)
            vehicleType = browser.find_element_by_xpath("//a[contains(@href,'fahrzeugfarbe')]").text.lower()
            logger.debug("Vehicle type is %s", vehicleType)
            vehicleStatus = browser.find_element_by_xpath('//span[contains(@class, "building_list_fms")]').text
            logger.debug("Vehicle type is %s", vehicleStatus)
            currVehicle = Vehicle(vehicleId,vehicleName,vehicleType,vehicleStatus)
            with open('../json/vehicles.json', 'w') as outfile:
              logger.debug("Building vehicle for JSON file")
              vdata['vehicles'][vehicleId] = {}
              vdata['vehicles'][vehicleId]['vehicleName'] = vehicleName
              vdata['vehicles'][vehicleId]['vehicleType'] = vehicleType
              # Always save the status as 1, otherwise if it not despatchable upon save, it never will be.
              vdata['vehicles'][vehicleId]['vehicleStatus'] = "1"
              logger.debug("Adding vehicle to JSON file")
              json.dump(vdata,outfile,sort_keys=True,indent=4)

          checked+=1
          logger.debug("Vehicle info built, adding to list")
          self.vehicleList.append(currVehicle)
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
      logger.info("Doing missions")
      for mission in self.missionList:
        logger.debug("Checking if %s has already been dispatched", mission.getName().encode("UTF-8"))
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
    randomsleep()

  def despatchVehicles(self,mission):
    """
      Despatch vehicles based on the passed mission's requirements \n
      Mission (MissionObj): The mission to be despatched
    """
    logger.info("Dispatching vehicles to %s",mission.getName().encode("UTF-8"))
    print(f"Going to mission {mission.getName()}")
    logger.debug("Visiting the url")
    browser.get(BASE_URL + "missions/"+mission.getID())
    loaded = self.pageloaded()
    if loaded:
      print("Checking requirements for " + mission.getName())
    despatchedVehicles = []
    logger.debug("Going through the requirements")
    try:
      logger.debug("Checking if there's a missing vehicles button")
      if browser.find_element_by_xpath("//a[contains(@href,'missing_vehicles')]"):
        logger.debug("Clicking missing vehicles button")
        browser.find_element_by_xpath("//a[contains(@href,'missing_vehicles')]").click()
    except (NoSuchElementException,ElementClickInterceptedException) as e:
      logger.debug("Could not find missing vehicles")
    for requirement in mission.getRequirements():
      todes = int(requirement['qty'])
      logger.debug("%s %s are needed",todes,requirement['requirement'].encode("UTF-8"))
      des = 0
      checkedunits = False
      logger.debug("Going through the requirements and the user's vehicles to dispatch")
      try: 
        for category in vehicles:
          #Only need to check for required types
          if requirement['requirement'] == category.lower():
            print("Mission needs "+str(todes)+" " + category)
            for vehicle in vehicles[category]:
              vehicle = vehicle.lower()
              try:
                checkboxes = browser.find_elements_by_xpath("//input[contains(@id,'vehicle_checkbox')]")
                # Check the checkboxes against our vehicle, see if the checkbox is available.
                for checkbox in checkboxes:
                  if(des<todes):
                   logger.debug("Mission still needs vehicles, despatching.")
                  #   For each vehicle in our available list
                   for ownedVehicle in self.vehicleList:
                    #  Check the type is what we need, and available for despatch
                    if(ownedVehicle.getType() == vehicle and (ownedVehicle.despatchable())):
                      logger.debug("User has %s %s available",ownedVehicle.getType().encode("UTF-8"),category.encode("UTF-8"))
                      #print("We have a " + category + " " + ownedVehicle.getType() + " available")
                      #vehicleStatus = browser.find_element_by_xpath('//span[contains(@class, "building_list_fms")]').text  
                      
                      # If amount of despatched is less than required.
                      logger.debug("Checking if there required quantity as been achieved")  
          
                        # If the checkbox ID is that for the vehicle, scroll to and click.
                      if checkbox.get_attribute('value') == ownedVehicle.getID():
                        logger.debug("There is a checkbox with the id "+ownedVehicle.getID() )             
                        browser.execute_script("arguments[0].scrollIntoView();", checkbox)
                        checkbox.click()
                        checkedunits = True     
                        des+=1
                        logger.debug("Adding vehicle to despatched list, and setting it as despatched")
                        despatchedVehicles.append(ownedVehicle.getID())   
                        ownedVehicle.setDespatched()       
              except (NoSuchElementException, ElementClickInterceptedException) as e: 
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
      # If the requirement is ambulance, and it's been submitted- this code should also work for  police etc.
      if(requirement['requirement'])=="ambulance":
        browser.get(BASE_URL + "missions/"+mission.getID())
        try:
          # Wait first couple seconds to wait for JS to init the time.
          time.sleep(2)
          remaining = browser.find_elements_by_xpath('//td[contains(@id, "vehicle_drive")]')[0].text
          mins = int(remaining.split(":")[0].replace(":","")) * 60
          seconds = int(remaining.split(":")[1].replace(":",""))
          wait = (mins + seconds) * 2
          print(f"Ambulance waiting {wait} seconds to despatch patient")
          time.sleep(wait)
          browser.get(BASE_URL + "missions/"+mission.getID())
          browser.refresh();
          browser.find_element_by_id("process_talking_wish_btn").click()
          browser.find_elements_by_xpath('//a[contains(@href, "patient")]')[0].click()
        except NoSuchElementException as e:
         logger.debug("Is ambulance but no patient to send anywhere..")

      print(f"{des} units despatched")
      logger.debug("%s vehicles have been despatched", des)

      logger.debug("Checking if missions is in our despatches list")
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
    with open("./debug/debug.log", "a") as log:
      log.write("")
      
def login(username,password):
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
  requirementId = requirementsurl.split("?")[0].split("/")[4]
  rfile = "../json/missions/" + SERVER  + '/' + requirementId + '.json'
  # If we have generated the missions, and the file exists.
  if(os.path.exists(rfile) == True):
    # Open the file get the requirements and return them, as they're previously saved (not via cache)
    with open(rfile,encoding="utf8") as requirementfile:
     return json.load(requirementfile)['requirements']
    #  Else, either we don't have the mission saved, or - somehow we don't know it. Find requirements manually and return.
  else:
    logger.debug("Visiting %s",requirementsurl)
    browser.get(requirementsurl)
    requiredlist = []
    logger.debug("Grabbing table elements")
    requirements = browser.find_elements_by_tag_name('table')[1].find_elements_by_tag_name('td')
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
    logger.debug("Looping through the table to extract each vehicle")
    for index, r in enumerate(requirements):
     if r.text.isdigit() == False and len(r.text)>0:
        requirement =  r.text.replace('Required','').replace('Wymagane','').replace('Wymagany','').replace('Требуемые','').replace("Benodigde",'').replace("benodigd",'').replace("Nödvändiga","").replace("richieste","").replace("richiesti","").replace("richiesta","").replace("Benötigte","").strip().lower()
        qty = requirements[index+1].text
        print(f"Requirement found : {str(qty)} x {str(requirement)}")
        requiredlist.append({'requirement':requirement,'qty': qty })
    print(Fore.YELLOW + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"+Style.RESET_ALL)
    if(len(requiredlist)==0):
     logger.warning("No requirements were found, appending 1 ambulance?")
     requiredlist.append({'requirement':'ambulance','qty': 1 })
    return requiredlist

  


logger = setup_logger('botLogger','debug.log',level=logging.CRITICAL)
operatingsystem = platform.system()
path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read('../config/config.ini')
#BASE_URL = config['DEFAULT']['url']
SERVER = config['DEFAULT']['server']
MISSION_BATCH_NUM = int(config['DEFAULT']['mission_batch_amount'])
username = config['DEFAULT']['email'].strip()
password = config['DEFAULT']['password'].strip()
#print("Selected server ", SERVER)

servers = configparser.ConfigParser()
servers.read('../config/server.ini')
BASE_URL = servers[SERVER]['url']
SERVER_REGION = servers[SERVER]['name']


# Check and install chrome driver to path depending on the os.
chromedriver_autoinstaller.install() 

chrome_options = Options()  
if config['DEFAULT'].getboolean('headless_mode') == True:
  chrome_options.add_argument("--headless")  

if "pytest" in sys.modules:
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
browser = webdriver.Chrome(options=chrome_options)

  # Load vehicles from our json file.
with open('../json/vehicles/'+SERVER+'/vehicles.json',encoding="utf8") as reqlink:
  vehicles = json.load(reqlink)

  
def begin(): 
 MissonChiefBot()

if __name__ == '__main__':
 try:
      begin()
 except KeyboardInterrupt:
  print('Closing..')
  logger.debug("Closing bot.")
  try:
   sys.exit(1)
  except SystemExit:
   os._exit(1)