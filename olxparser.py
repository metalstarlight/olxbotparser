from config import URL, DRIVER_PATH
from db import process_add_express, find_all_searches
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC#, expected_conditions
from selenium.common.exceptions import TimeoutException
from db import process_add_express

service = Service()
browser = webdriver.Chrome(service=service)
#browser.minimize_window()

async def get_parsed_elements(URL: str):

    browser.get(url=URL)
    time.sleep(5)
    try:
        elemAkceptuje = browser.find_element(By.ID,"onetrust-accept-btn-handler")
        ActionChains(browser).click(elemAkceptuje).perform()
    except:
        pass
    while True:
        try:
            element = WebDriverWait(driver=browser, timeout=2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "css-rc5s2u"))) #Block "css-1ut25fa" (with image), change to your class
            for i in range(len(element)):
                 text = element[i].text
                 lines = text.splitlines()
                 title = lines[0]
                 price = lines[1]
                 whereAndDate = lines[3]
                 url = element[i].get_attribute("href")
                 #img_png = element[i].find_element(By.XPATH, ".//div[@class='css-1ut25fa']").screenshot_as_png          #(By.CLASS_NAME, "css-1av34ht").screenshot_as_png
                 #(By.XPATH, ".//div[@class='css-1ut25fa']").screenshot_as_png
                 #print(type(img_png))
                 await process_add_express(title=title, price=price, whereAndDate=whereAndDate, url=url) #image=img_png    в аргументах
            #print(element.get_attribute("href")) # Взять ссылку на блок
            break
        except TimeoutException as _ex:
            print(_ex)
            break