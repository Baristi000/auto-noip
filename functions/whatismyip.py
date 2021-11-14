from time import sleep

from functions.noip import genDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_elements(driver, locator: tuple):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(locator)
    )

def getCurrentIp(separate_driver):
    separate_driver.get("https://whatismyipaddress.com")
    ip = wait_elements(separate_driver, (By.XPATH, '//span[@class="address"][@id="ipv4"]')).text
    for i in range(5):
        if "Checking..." in ip:
            sleep(1)
            ip = wait_elements(separate_driver, (By.XPATH, '//span[@class="address"][@id="ipv4"]')).text
            separate_driver.execute_script("window.stop();")
    print("Current IP:\t", ip)
    return ip