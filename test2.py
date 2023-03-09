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



# Open the file containing links
from parsel import Selector


with open('items.txt', 'r') as f:
    # Read the first line in the file
    link = f.readline().strip()
driver.get(link)
sel = Selector(text=driver.page_source)
name = sel.xpath('//h1/text()')
print(name)