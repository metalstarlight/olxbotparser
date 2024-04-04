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

# Надо сделать скрипт который раз в 29 секунд обновляет сайт и вытаскивает новые карточки, добавляет в базу данных и отправляет новые в телеграм.

service = Service()
browser = webdriver.Chrome(service=service)
URI = "https://www.olx.pl/elektronika/sprzet-agd/warszawa/q-ekspress-do-kawy/?search%5Bfilter_enum_state%5D%5B0%5D=damaged&search%5Bfilter_enum_state%5D%5B1%5D=used"

def get_source_code(URI: str) -> None:

    browser.get(url=URI)
    time.sleep(3)
    elemAkceptuje = browser.find_element(By.ID,"onetrust-accept-btn-handler")
    ActionChains(browser).click(elemAkceptuje).perform()
    while True:
        try:
            element = WebDriverWait(driver=browser, timeout=2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "css-rc5s2u")))
            for i in range(len(element)):
                 print(element[i].text, element[i].get_attribute("href"))
            #print(element.get_attribute("href")) # Взять ссылку на блок
            break
        except TimeoutException as _ex:
            print(_ex)
            break
    

def main() -> None:
    get_source_code(URI)

if __name__ == "__main__":
    main()