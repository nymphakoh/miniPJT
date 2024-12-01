#상세페이지 URL 크롤링
#from numpy.distutils.conv_template import header
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from tqdm import trange


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
def CrawlingPlaceInfo(url,driver):
    try:
        # response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()  # HTTP 오류가 있는 경우 예외 발생
        # soup = BeautifulSoup(response.text, 'html.parser')
        tit_location=""
        star=""
        reviewCount=""
        tag_list=[]
        driver.get(url)
        # print(driver)
        # print(lists)
        #별점과 개수 가져오기
        lists = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'location_evaluation')))
        star = lists.find_element(By.CLASS_NAME,'color_b').text
        reviewCount_ = lists.find_element(By.CLASS_NAME,'color_g').text
        reviewCount = re.sub(r'\((\d+)\)', r'\1', reviewCount_)
        print(star,reviewCount)
        # lists = soup.find(class_='location_evaluation')
        # star = lists.find(class_='color_b').get_text(strip=True) if lists else ''
        # review_count = lists.find(class_='color_g').get_text(strip=True) if lists else ''
        # print(star, review_count)

        #가게 이름 가져오기
        div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'place_details')))
        tit_location = div.find_element(By.CLASS_NAME,'tit_location').text
        print(tit_location)
        # div = soup.find(class_='place_details')
        # tit_location = div.find(class_='tit_location').get_text(strip=True) if div else ''
        # print(tit_location)

        #테그 가져오기
        div2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'details_placeinfo')))
        tags = div2.find_elements(By.CLASS_NAME,'link_tag')
        # div2 = soup.find(class_='details_placeinfo')
        # tags = div2.find_all(class_='link_tag') if div2 else []
        # tag_list = [tag.get_text(strip=True) for tag in tags]
        if tags:
            for tag in tags:
                tag_list.append(tag.text)
            print(tag_list)
    except Exception as e:
        print("오류가 발생했습니다:", e)
    finally:
        # 크롤링한 데이터를 딕셔너리로 정리
        data = {
            "가게 이름": tit_location,
            "별점": star,
            "리뷰 수": reviewCount,
            "태그들": ", ".join(tag_list)  # 태그를 쉼표로 구분된 문자열로 변환
        }
        return data

# Load the uploaded CSV file
# CSV 파일 경로 설정
input_csv_path = '/Users/jejinan/Desktop/새싹/cafes3.csv'
output_csv_path = '/Users/jejinan/Desktop/새싹/cafe3_infos.csv'

# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)
# 사용자 에이전트 설정 (웹사이트가 자동화된 요청을 차단하지 않도록)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
#                   'AppleWebKit/537.36 (KHTML, like Gecko) ' \
#                   'Chrome/115.0.0.0 Safari/537.36'
# }

try:
    data = pd.read_csv(input_csv_path)
    place_infos = []
    # Extract the 'place_url' column
    place_url_list = data['place_url'].tolist()
    print(len(place_url_list))
    for url in tqdm(place_url_list):
        place_infos.append(CrawlingPlaceInfo(url, driver))
    print(place_infos)

    df_place_infos = pd.DataFrame(place_infos)

    df_place_infos.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"데이터가 '{output_csv_path}' 파일로 저장되었습니다.")
except Exception as e:
    print("스크래핑 도중 오류가 발생했습니다:", e)
finally:
    # WebDriver 세션 종료
    driver.quit()
    print("WebDriver 세션이 종료되었습니다.")