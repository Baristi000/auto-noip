from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Tạo ra driver
def genDriver(headless:bool=False):
    o = webdriver.ChromeOptions()
    o.add_argument("disable-features=VizDisplayCompositor")
    if headless:
        o.add_argument("headless")
    o.add_argument("window-size=1200x800")
    o.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0")
    driver = webdriver.Chrome(options=o)
    print("Generate driver!")
    return driver
# Đăng nhập vào noip
def login(driver, username: str, password: str):
    print("Login ...")
    driver.get("https://my.noip.com/")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    login = driver.find_element_by_xpath('//*[@type="submit"]').click()
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content-wrapper"]//span[text()[contains(.,"Active")]]')))
    driver.get("https://my.noip.com/dynamic-dns")
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//a[@class="link-info cursor-pointer"]')))
    print("Login succeed!")
# Lấy tất cả các host hiện có
def getAllHostName(driver):
    pos = driver.find_elements_by_xpath('//a[@class="link-info cursor-pointer"]')
    hosts = []
    for item in pos:
        hosts.append(item.text)
    print("Found host(s):\t", hosts)
    return hosts
# Lấy ngày hết hạn của host được cấp
def getExpireDateFromHost(driver, host:str):
    host_list = driver.find_elements_by_xpath('//a[@class="link-info cursor-pointer"]')
    ex_list = driver.find_elements_by_xpath('//*[@id="host-panel"]//div/a')
    for i in host_list:
        if i.text == host:
            ex_date = ex_list[host_list.index(i)].text.split(" ")[2]
            print("Expire date:\t", ex_date)
            return ex_date
# Lấy ip của host được cấp
def getIpFromHost(driver, host:str):
    host_list = driver.find_elements_by_xpath('//a[@class="link-info cursor-pointer"]')
    ip_list = driver.find_elements_by_xpath('//td[@data-title="IP / Target"]')
    for i in host_list:
        if i.text == host:
            ip = ip_list[host_list.index(i)].text
            print("Ip:\t\t", ip)
            return ip
# Làm mới lại host theo ip cung cấp
def renew(driver, host:str, ip: str):
    dels = driver.find_elements_by_xpath('//div[@data-cy="remove-hostname"]')
    hosts = getAllHostName(driver)
    dels[hosts.index(host)].click()
    ele = driver.find_element_by_xpath('//button[@data-cy="delete"]')
    driver.execute_script("arguments[0].click();", ele)
    ele = driver.find_element_by_xpath('//button[text()[contains(.,"Create Hostname")]]')
    # wait until succeed
    sleep(2)
    # conts job
    driver.execute_script("arguments[0].click();", ele)
    # wait until succeed
    sleep(1)
    # conts job
    ele = driver.find_element_by_xpath('//input[@id="name"][@placeholder="myhost"]')
    driver.execute_script("arguments[0].click();", ele)
    ele.send_keys(host.split(".")[0])
    ele = driver.find_element_by_xpath('//input[@data-cy="ipv4-address"]')
    driver.execute_script("arguments[0].click();", ele)
    ele.send_keys(ip)
    ele = driver.find_element_by_xpath('//*[@id="host-modal"]/div/div/div[4]/button[1]').click()
    ele = driver.find_elements_by_xpath
    print("Renew succeed!")
    sleep(1)

# Tìm các host đang sắp hết hạn 
def renewAll(driver, ip:str):
    hosts = getAllHostName(driver)
    for host in hosts:
        print("check host:\t", host)
        sleep(10)
        renew(driver, host, ip)

# Test code
def test():
    # Thông tin người dùng
    username = "baristi000"
    password = "Trieukute_2420"

    # Tạo driver
    driver = genDriver(headless=False)
    # Đăng nhập
    login(driver, username, password)
    # Lấy các hosts
    hosts = getAllHostName(driver)
    # xem ngày hết hạn 
    getExpireDateFromHost(driver,hosts[0])
    # Làm mới
    renew(
        driver, 
        hosts[0], 
        getIpFromHost(
            driver, 
            hosts[2])
        )
    # Đóng driver
    driver.close()