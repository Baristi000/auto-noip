from functions.noip import renewAll, genDriver, login
from functions.whatismyip import getCurrentIp
import time

username = "baristi000"
password = "Trieukute_2420"

SLEEP_TIME = 60*60*24*1

while True:
    driver = genDriver(headless=True)
    print("********************")
    ip = getCurrentIp(driver)
    print("********************")
    login(driver, username, password)
    print("********************")
    renewAll(driver, ip)
    print("********************")
    driver.close()
    time.sleep(SLEEP_TIME)