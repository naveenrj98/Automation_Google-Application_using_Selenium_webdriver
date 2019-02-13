import time
from selenium import webdriver
from selenium.webdriver import ActionChains


driver = webdriver.Chrome("G:\\PROJECTS BMSCE\\NRJ&NRV\\chromedriver")
#driver.get("https://google.com")

driver.get("http://bing.com")

#ele = driver.find_elements_by_tag_name('body').send_keys(Keys.CONTROL + 't')

driver.execute_script("window.alert('Your going to automating the login page');")

time.sleep(5)
driver.switch_to.alert
