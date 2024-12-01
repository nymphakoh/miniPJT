
from selenium import webdriver #동적크롤링
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

driver = webdriver.Chrome()

url = "https://m.map.kakao.com/"
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

driver.get(url)

# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 카카오맵 검색
search_keyword = "창동역 카페"
url = "https://map.kakao.com/"
driver.get(url)
time.sleep(2)

'''# 검색창에 키워드 입력
search_box = driver.find_element(By.ID, "search.keyword.query")
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)
time.sleep(2) #페이지 로드 대기'''

# "주변" 버튼 클릭
try:
    nearby_button = driver.find_element(By.CSS_SELECTOR, "div.option button[data-id='btnNearby']")
    nearby_button.click()
    time.sleep(2)
except Exception as e:
    print(f"주변 버튼 클릭 실패: {e}")
    driver.quit()

# "카페" 버튼 클릭
try:
    cafe_button = driver.find_element(By.CSS_SELECTOR, "button[data-category='카페']")
    cafe_button.click()
    time.sleep(3)
except Exception as e:
    print(f"카페 버튼 클릭 실패: {e}")
    driver.quit()


# 카페 리스트 가져오기
cafe_data = []
while True:
    # 검색 결과 가져오기
    items = driver.find_elements(By.CSS_SELECTOR, ".placelist > .PlaceItem")
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, ".link_name").text
            rating = item.find_element(By.CSS_SELECTOR, ".rating > .score").text
            address = item.find_element(By.CSS_SELECTOR, ".addr").text
            cafe_data.append({"name": name, "rating": rating, "address": address})
        except Exception as e:
            # 별점이 없는 경우 예외 발생
            print(f"Error extracting data: {e}")
            continue

    # 다음 페이지 이동
    try:
        next_button = driver.find_element(By.ID, "info.search.page.next")
        if "disabled" in next_button.get_attribute("class"):
            break  # 다음 버튼이 비활성화면 종료
        next_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

# 결과 출력
for cafe in cafe_data:
    print(cafe)

# WebDriver 종료
driver.quit()


