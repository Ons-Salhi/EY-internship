# importing libraries and packages for this project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import urllib
import collections
collections.Callable = collections.abc.Callable
import pandas as pd

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
    time.sleep(3)
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
print(links)

file = open(search_query+'.txt','w',encoding='utf-8')
for item in l:
    if ('www.linkedin.com/in/' in item):
	    file.write(item+"\n")
file.close()



with open('scraped.txt','w',encoding='utf-8') as t:

    with open(search_query+'.txt', 'r',encoding='utf-8') as f:
        # Read the first line in the file
        link = f.readlines()
    for i in link:
        try:
            driver.get(i)
            time.sleep(5)
            name = driver.find_element(By.XPATH, '//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]')
            try:
                for i in name:
                    t.write(i.get_attribute('innerHTML'))
            except:
                t.write(name.get_attribute('innerHTML'))

            time.sleep(2)

            location = driver.find_elements(By.XPATH, '//span[@class="text-body-small inline t-black--light break-words"]')
            try:
                for i in location:
                    t.write(i.get_attribute('innerHTML'))
            except:
                t.write(location.get_attribute('innerHTML'))   

            time.sleep(1)

            title = driver.find_elements(By.XPATH, '//div[@class="text-body-medium break-words"]')
            try:
                for i in title:
                    t.write(i.get_attribute('innerHTML'))
            except:
                t.write(title.get_attribute('innerHTML'))

                time.sleep(3)

            experience_info = driver.find_elements(By.XPATH,'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[*]')
            try:
                for i in experience_info:
                    t.write(i.text)
                    t.write('\n#######\n')
            except:
                t.write(experience_info.get_attribute('outerHTML'))  
                
            t.write('\n__________________________________________\n')
        except:
            continue

import csv

# Define the headers for the CSV
headers = ['Name', 'Location', 'Title', 'About', 'Featured', 'Experience', 'Education',
           'Licenses & certifications', 'Skills', 'Recommendations', 'Interests']

# Open the text file with utf-8 encoding
with open('scraped.txt', 'r', encoding='utf-8') as file:
    data = file.read()

people_data = data.strip().split('\n__________________________________________\n')

with open(search_query+'.csv', mode='w', encoding='utf-8', newline='') as output_file:
    writer = csv.writer(output_file)
    
    # Write the headers to the first row of the CSV
    writer.writerow(headers)

    for i in people_data:
        row_data = {
            'Name': '',
            'Location': '',
            'Title': '',
            'About': '',
            'Featured': '',
            'Experience': '',
            'Education': '',
            'Licenses & certifications': '',
            'Skills': '',
            'Recommendations': '',
            'Interests': ''
        }

        lines = i.split('\n')
        row_data['Name'] = lines[0]
        row_data['Location'] = lines[1]
        row_data['Title'] = lines[3]
        
        sections = i.split("#######")[1:-1]
        for section in sections:
            section_name, section_content = section.split('\n', 1)
            section_variable_content = section_content.strip()
            unique_content = '\n'.join(set(section_variable_content.splitlines()))
            section_variable_name = section_variable_content.split('\n')[0]

            # If the section variable name matches one of the headers, add its content to the row_data
            if section_variable_name in headers:
                row_data[section_variable_name] = unique_content

        # Write the row data to the CSV
        writer.writerow([row_data[header] for header in headers])
        

df = pd.DataFrame(pd.read_csv('./HR.csv'))
df.to_excel('HR.xlsx')