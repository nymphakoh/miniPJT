#from numpy.distutils.conv_template import header
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = Options()
#chrome_options.add_argument("headless")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://place.map.kakao.com/23941455')
#print(driver)
time.sleep(1)

#print(lists)

#별점과 개수 가져오기
lists = driver.find_element(By.CLASS_NAME, 'location_evaluation')
star = lists.find_element(By.CLASS_NAME,'color_b').text
reviewCount = lists.find_element(By.CLASS_NAME,'color_g').text
print(star,reviewCount)

#가게 이름 가져오기
txt_address = driver.find_element(By.CLASS_NAME,'txt_address').text
print(txt_address)

#도로명주소 가져오기
div = driver.find_element(By.CLASS_NAME, 'place_details')
tit_location = div.find_element(By.CLASS_NAME,'tit_location').text
print(tit_location)

#태그 가져오기
tag_g = driver.find_element(By.CLASS_NAME,'tag_g').text
print(tag_g)

driver.quit()