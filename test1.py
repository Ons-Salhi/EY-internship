# importing libraries and packages for this project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import urllib
import collections
collections.Callable = collections.abc.Callable

print('finished importing')
search_query = input('What type of profile do you want to scrape?')
number_of_pages = int(input('How many pages do you want to scrape?'))
# Access linkedin and login 
driver = webdriver.Edge()
url = 'https://www.linkedin.com/login'
driver.get(url)
print('Finished initializing a driver')
time.sleep(1)

# Import username and password
creds_path =  os.path.join(os.path.abspath(os.path.dirname(__file__)), 'login_credential.txt')
credential = open(creds_path)
line = credential.readlines()
username = line[0]
password = line[1]
print('Finished importing login credentials')

# Enter your username
email_field = driver.find_element(By.ID,'username').send_keys(username + Keys.ENTER)
print('Finished entering email')
time.sleep(2)

# Enter your password
password_field = driver.find_element(By.NAME,'session_password').send_keys(password)
print('Finished entering password')
time.sleep(1)

# Click login button
login_field = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button[1]')
login_field.click()
print('Successfully logged in!')
time.sleep(2)



profile_to_find = urllib.parse.quote(search_query)
url = 'https://www.linkedin.com/search/results/people/?keywords='+profile_to_find+'&origin=SWITCH_SEARCH_VERTICAL&page='
links=[]


def extract_links(i):
    url = 'https://www.linkedin.com/search/results/people/?keywords='+profile_to_find+'&origin=SWITCH_SEARCH_VERTICAL&page='+str(i)
    driver.get(url)
    time.sleep(1)
    profiles = driver.find_elements(By.CLASS_NAME,'app-aware-link')
    profile_links = []
    for profile in profiles:
        profile_links.append(profile.get_attribute("href"))
    for link in profile_links:
        links.append(link)
for i in range(1,number_of_pages+1):
    time.sleep(4)
    extract_links(i)
    print('going to page '+str(i))
l=set(links)

file = open(search_query+'.txt','w')
for item in l:
    if ('www.linkedin.com/in/' in item):
	    file.write(item+"\n")
file.close()
