from selenium import webdriver
import time
import cv2
k = 0
import os
from selenium.webdriver.common.keys import Keys

def comand(comd):
    op = os.popen(comd).read()
    return op

driver = webdriver.Chrome("G:\chromedriver_win32\chromedriver.exe")
driver.get("https://web.whatsapp.com/")
time.sleep(15)
name = input('name = ')
person = driver.find_element_by_xpath('//*[@title="' + name + '"]')
print('Opened contact named' + person.text)    
person.click()
while True:
    msgtag = driver.find_elements_by_xpath("//*[@class='emojitext selectable-text']")
    if msgtag[-1].text[-2:] == ':)':
        time.sleep(1)
        continue
    try:
        op = comand(msgtag[-1].text)        
        text = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        text.send_keys(op)
        text.send_keys(Keys.RETURN)
        text = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        text.send_keys('comand recieved :)')
        text.send_keys(Keys.RETURN)
    except:
        text = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        text.send_keys('invalid comand :)')
        text.send_keys(Keys.RETURN)
    if msgtag[-1].text == 'exit':
        break
    time.sleep(10)
    


"""while k<5:
    elem = driver.find_element_by_xpath(//*[@id="main"]/div[2]/div/div/div[3]/div[19]/div/div/div/div[1]/span[2])
    word = elem.text
    print(word)
    inp = driver.find_element_by_xpath(//*[@id="main"]/footer/div[1]/div[2]/div/div[2])
    inp.send_keys(word)
    inp.send_keys(Keys.RETURN)
    k = k+1
"""
driver.close()
