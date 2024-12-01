'''import requests

# Kakao REST API 키를 입력하세요
REST_API_KEY = '540340bf98df8f8881eff5793565caee'

# 요청 헤더 설정
headers = {
    "Authorization": f"KakaoAK {REST_API_KEY}"
}
i=0
while True:
    i+=1
    # 요청 파라미터 설정 
    params = {
        'category_group_code': 'FD6',       # 음식점 카테고리 코드
        'x': '127.04983663744756',                 # 중심 좌표의 경도 (서울 시청 기준)
        'y': '37.6541800252641',                   # 중심 좌표의 위도
        'radius': '500',                    # 검색 반경 (미터 단위, 최대 20,000)
        'page': str(i),                        # 페이지 번호
        'size': '15',                       # 한 페이지에 보여질 문서의 개수
        'sort': 'distance'                  # 거리순 정렬
    }

    # 카카오 로컬 API URL
    url = 'https://dapi.kakao.com/v2/local/search/category.json'

    # API 요청 보내기
    response = requests.get(url, headers=headers, params=params)

    # 응답 상태 코드 확인
    if response.status_code == 200:
        data = response.json()
        for place in data['documents']:
            print(f"상호명: {place['place_name']}")
            print(f"카테고리 : {place['category_name']}")
            print(f"주소: {place['address_name']}")
            print(f"전화번호: {place['phone']}")
            print(f"place_url : {place['place_url']}")
            print(f"위도: {place['y']}, 경도: {place['x']}")
            print("-" * 40)

        if data['meta']['is_end']:
            print(f"모든 페이지를 가져왔습니다. end at {i}")
            break
    else:
        print(f"에러 발생: {response.status_code} {response.reason}")
        break
    print("@"*15,f"page : {i}","@"*15)'''


import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# print(ChromeDriverManager().install())
# Kakao REST API 키를 입력하세요
REST_API_KEY = '540340bf98df8f8881eff5793565caee'

CHROME_DRIVER_PATH = r"C:\Users\r2com\.wdm\drivers\chromedriver\win64\131.0.6778.85\chromedriver-win32/chromedriver.exe"  # ChromeDriver가 위치한 경로 입력
service = Service(CHROME_DRIVER_PATH)


# Selenium 브라우저 설정
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # 브라우저를 띄우지 않도록 설정
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())

# 요청 헤더 설정
headers = {
    "Authorization": f"KakaoAK {REST_API_KEY}"
}

i = 0
with webdriver.Chrome(service=Service, options=options) as driver:
    while True:
        i += 1
        # 요청 파라미터 설정
        params = {
            'category_group_code': 'FD6',       # 음식점 카테고리 코드
            'x': '127.04983663744756',          # 중심 좌표의 경도
            'y': '37.6541800252641',            # 중심 좌표의 위도
            'radius': '500',                    # 검색 반경
            'page': str(i),                     # 페이지 번호
            'size': '15',                       # 한 페이지에 보여질 문서의 개수
            'sort': 'distance'                  # 거리순 정렬
        }

        # 카카오 로컬 API URL
        url = 'https://dapi.kakao.com/v2/local/search/category.json'

        # API 요청 보내기
        response = requests.get(url, headers=headers, params=params)

        # 응답 상태 코드 확인
        if response.status_code == 200:
            data = response.json()
            for place in data['documents']:
                print(f"상호명: {place['place_name']}")
                print(f"카테고리 : {place['category_name']}")
                print(f"주소: {place['address_name']}")
                print(f"도로명 주소: {place.get('road_address_name', '정보 없음')}")
                print(f"전화번호: {place['phone']}")
                print(f"place_url : {place['place_url']}")
                print(f"위도: {place['y']}, 경도: {place['x']}")
                print("-" * 40)

                # Selenium을 이용하여 평점 크롤링
                try:
                    place_url = place['place_url']
                    driver.get(place_url)
                    time.sleep(2)  # 페이지 로드 대기
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # 별점 정보 추출 (HTML 구조에 따라 Selector 수정 필요)
                    rating_element = soup.select_one('.num_rate')
                    if rating_element:
                        rating = rating_element.text.strip()
                        print(f"평점: {rating}")
                    else:
                        print("평점을 찾을 수 없습니다.")
                except Exception as e:
                    print(f"평점 크롤링 중 오류 발생: {e}")

            if data['meta']['is_end']:
                print(f"모든 페이지를 가져왔습니다. 끝 페이지: {i}")
                break
        else:
            print(f"에러 발생: {response.status_code} {response.reason}")
            break
        print("@" * 15, f"page : {i}", "@" * 15)



