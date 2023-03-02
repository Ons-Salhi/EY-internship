# importing libraries and packages for this project

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup

print('finished importing')
search_query = input('What type of profile do you want to scrape?')
number_of_pages = int(input('how many pages do you want to scrape'))
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

# Locate the search bar element
try:
    search_button_mini = driver.find_element(By.XPATH,'//*[@id="global-nav-search"]/div/button')
    search_button_mini.click()
    time.sleep(1.5)
except:
    time.sleep(0.1)

# Input the search query to the search bar
search_field = driver.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input')
search_field.send_keys(search_query)
time.sleep(1)





# Search
search_field.send_keys(Keys.ENTER)
def extract_links():
    time.sleep(5)
    links = []
    elems = driver.find_elements(By.XPATH,"//a[@href]")
    for elem in elems:
        if 'https://www.linkedin.com/in/' in elem.get_attribute("href"):
            links.append(elem.get_attribute("href"))
    non_duplicate_links=set(links)
    return non_duplicate_links
def go_to_next_page():
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
    time.sleep(2)
    next_button = driver.find_element(By.CLASS_NAME,"artdeco-pagination__button--next")
    next_button.click()
    time.sleep(1)



global_links=[]

for i in range(number_of_pages):
    global_links.extend(extract_links())
    time.sleep(4)
    go_to_next_page()
for i in global_links:
    print(i)
