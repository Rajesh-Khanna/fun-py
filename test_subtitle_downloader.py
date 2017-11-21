from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,time
import zipfile
cout = 0
name = input('movie name = ')
name = name.split(' ')
destination = input('movie folder = ')
driver = webdriver.Chrome("G:\chromedriver_win32\chromedriver.exe")
driver.get('http://www.moviesubtitles.org/')
elem = driver.find_element_by_xpath('''//*[@id="search"]/form/p/input[1]''')
for keys in name:
    elem.send_keys(keys + ' ')
elem.send_keys(Keys.RETURN)
#
try:
    links = driver.find_elements_by_partial_link_text(name[0])
    for element in links :
        for c in name:
            if c in element.text:
                cout = cout + 1
            else:
                break
        if cout == len(name):
            break
        else:
            cout = 0
    key = element
except Exception as e:
    print(e)
    quit()
if not cout == len(name):
    print('Subtitles for that movie are not available')
    quit()
cout = 0
key.click()
#download = driver.find_element_by_xpath('''//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[10]/td/a/nobr[1]/h3/img''')
download = driver.find_element_by_css_selector('''#content > div.left > div > table > tbody > tr:nth-child(3) > td > div > div > a:nth-child(2)''')
download.click()
download = driver.find_element_by_xpath('''//*[@title="Download"]''')
download.click()                          #//*[@id="content"]/div[3]/div/div[2]/table/tbody/tr[10]/td/a/nobr[1]/h3/img
downloaddir = "C:\\Users\\Rajesh Khanna\\Downloads\\" 
os.chdir(downloaddir)
time.sleep(5)
for f in os.listdir():
    f_name = f.split('_')
    f_name = ' '.join(f_name)
    #print(f_name)
        
    for c in name:
        if c in f_name:
            cout = cout + 1
        else:
            break
    if cout == len(name):
        break
    else:
        cout = 0
cout = 0
movie_file = []
with zipfile.ZipFile(f) as zipf:
    subtitle_folder = destination +'\\'+ f_name
    zipf.extractall(subtitle_folder)
os.chdir(destination)
for f in os.listdir():
    f_name = f.split('_')
    f_name = ' '.join(f_name)
    #print(f_name)
    for c in name:
        if c in f_name:
            if not '.zip' in f_name:
                cout = cout + 1
        else:
            break
    if cout == len(name):
        movie_file.append(f)
    cout = 0
for f in movie_file:
    os.rename(f,subtitle_folder+'\\'+f)
