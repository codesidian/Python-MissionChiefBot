from splinter import Browser
import time
hrefs= [];
# Get URL from file
with open('url.txt', 'r') as f:
    baseurl = f.readline().strip()

def init():
    logged_in = login(username,password)
    if logged_in:
     while True:
      getMissions()
      print("Sleeping for 45 seconds...")
      time.sleep(45)
    else: 
     print("Couldn't log in...")
def login(username,password):
    print("Logging in")
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
     return True;
    except splinter.exceptions.ElementDoesNotExist: 
     return False;

def getMissions():
    print("Getting missions");
    url = baseurl
    browser.visit(url)
    # Finding links for missions
    try:
        links = browser.find_link_by_partial_href('/missions/')
        print(str(len(links)) + " missons found");
        for link in links: 
         hrefs.append(link['href'])
        doMissions();
    except:
        time.sleep(1)

def doMissions():
 count = 0
 for href in hrefs:
  time.sleep(5);   
  count+=1  
  mission_str = str(count);
  try:
   print("MISSION " + mission_str +":" + " VISITING MISSION")
   browser.visit(href)
  except:
   print("MISSION " + mission_str +":" + " COULDN'T GET LINK")
  try:
   print("MISSION " + mission_str +":" + " SELECTING UNIT TO DESPATCH")   
   checkbox=browser.find_by_css('input[class="vehicle_checkbox"]')
   for check in checkbox:
    check.check()
  except:
   print("MISSION " + mission_str +":" + " NO UNITS TO DESPATCH")   
  try:
   browser.find_by_name('commit').click()
   print("MISSION " + mission_str +":" + " ATTEMPTED TO DESPATCH.")   
  except:
   print("MISSION " + mission_str +":" + "CAN NOT DESPATCH A UNIT, OR UNIT ALREADY DESPATCHED")

    
# Taking account information from file
with open('account.txt', 'r') as f:
    username = f.readline().strip()
    password = f.readline().strip()
    

# Setting up browser

executable_path = {'executable_path':'./chromedriver.exe'}
browser = Browser('chrome', **executable_path)
init()