from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')


# Chrome 옵션 설정 (백그라운드 실행 가능)
chrome_options = Options()
#chrome_options.add_argument("--headless")  # 브라우저를 띄우지 않음
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-offline-load-stale-cache")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)


# WebDriver 실행
driver = webdriver.Chrome(options=chrome_options)

'''from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_argument("--lang=ko")

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.google.com')
# driver.find_element(By.CLASS_NAME,"gLFyf").send_keys("아이유")
# driver.find_element(By.CLASS_NAME,"gLFyf").send_keys(Keys.ENTER)

driver.find_element(By.CLASS_NAME, 'gLFyf').send_keys('아이유')
driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]").click()
driver.find_element(By.XPATH,'//*[@id="hdtb-sc"]/div/div/div[1]/div/div[3]/a').click()'''


try:
    # 크롤링할 카카오맵 URL
    url = "https://place.map.kakao.com/903557075"  # 별점이 있는 페이지 URL
    driver.get(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    # 페이지 로드 대기 (필요시 조정)
    time.sleep(5)

    # 식당이름 찾기 
    place_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="mArticle"]/div[1]/div/div[1]/h2'))
    ) 
    place_name = place_name_element.text

   
    # 별점 요소 찾기 
    #star_rating_element = driver.find_element(By.CLASS_NAME, "num_rate") 
    star_rating_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "color_b2"))
) 
    star_rating = star_rating_element.text
    
    print("식당명:", place_name)
    print("별점:", star_rating)

finally:
    # 브라우저 닫기
    driver.quit()
