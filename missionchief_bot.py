from splinter import Browser
import time
focus=0

def login(username,password):

    print("Logging in")
    # Visit URL
    url = "https://www.missionchief.com/users/sign_in"
    browser.visit(url)
    # Filling in login information
    browser.fill("user[email]",username)
    browser.fill("user[password]",password)
    # Submitting login
    browser.find_by_name('commit').click()
    
def doMissions():
   

    url = "https://www.missionchief.com"
    browser.visit(url)
    # Finding links for missions
    try:
        links = browser.find_link_by_partial_href('/missions/')
    except:
        time.sleep(1)

    # Opening the mission link

    try:
        browser.visit(links[focus]['href'])
    except:
        time.sleep(1)
    
    # Find the vehicle checkbox and check it
    try:
        #checkbox=browser.find_by_id('vehicle_checkbox_240277').check()
        checkbox=browser.find_by_xpath('//*[contains(@id, "checkbox")]').check()        
        
    except:
        time.sleep(1)

    # Submit the vehicle to the mission
    try:
        browser.find_by_name('commit').click()
    except:
        time.sleep(1)
    
    
        
    
# Taking account information from file
with open('account.txt', 'r') as f:
    username = f.readline().strip()
    password = f.readline().strip()

# Setting up browser

executable_path = {'executable_path':'./chromedriver.exe'}
browser = Browser('chrome', **executable_path)
login(username,password)
while True:
    try:
        if focus==1:
            focus=0
        else:
            focus=1
        doMissions()
    except:
        continue
    else:
        doMissions()
