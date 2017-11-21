from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
email = 'user name'
password = 'password'
driver = webdriver.Chrome("G:\chromedriver_win32\chromedriver.exe")
driver.get('https://www.facebook.com/events/birthdays/')
login = driver.find_element_by_xpath('''//*[@id="email"]''')
for keys in email:
    login.send_keys(keys)
#elem.send_keys(Keys.RETURN)
login = driver.find_element_by_xpath('''//*[@id="pass"]''')
for keys in password:
    login.send_keys(keys)
login.send_keys(Keys.RETURN)
i = 0
names = []
namesdiv = driver.find_elements_by_xpath('''//*[@class="clearfix _fbBirthdays__nameAndAge"]''')
print(len(namesdiv))
if(len(namesdiv) == 0):
    exit()
for elem in namesdiv:
    names.append(elem.find_element_by_xpath(".//a").text)
#time.sleep(10)
node = driver.find_elements_by_xpath('//*[@title="Write a birthday wish on his Timeline..."]')
node2 = driver.find_elements_by_xpath('//*[@title="Write a birthday wish on her Timeline..."]')
#node = node + node2
print(len(node))
for elem in node:

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    try:
        for keys in 'Happy Birthday ' + names[i] + '.... :)':
            elem.send_keys(keys)
        elem.send_keys(Keys.RETURN)
        elem.send_keys(Keys.RETURN)
    except:
        print('Error')
        a = input("sd")
        if a == 'q':
            exit()
    #login.send_keys(Keys.RETURN)
    i = i + 1
while(True):
    if(len(driver.find_elements_by_xpath('//*[@title="Write a birthday wish on his Timeline..."]'))==0):
        #driver.quit()
        break
    time.sleep(2)
'''
