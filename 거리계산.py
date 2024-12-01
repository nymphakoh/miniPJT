import pandas as pd
import numpy as np

point_place = {'latitude': 37.6545399298261, 'longitude': 127.049926290286}


# 데이터 (음식점 이름, 위도, 경도)
path = 'C:\\Users\\r2com\\Desktop\\수업자료\\mini_project\\'
data = pd.read_csv(path + 'restaurants3.csv', usecols= ['place_name','y','x'])
locations = pd.DataFrame(data)

# 현재 위치 (학원)
current_location = {'y': 37.6545399298261, 'x': 127.049926290286}

# Haversine 거리 계산 함수
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # 지구 반지름 (단위: km)
    # 각도를 라디안으로 변환
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    # 위도와 경도의 차이
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine 공식
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# 현재 위치와 각 장소 간의 거리 계산 후 새로운 컬럼 추가
locations["distance_from_current"] = locations.apply(
    lambda row: haversine(current_location["y"], current_location["x"], row["y"], row["x"]),
    axis=1
)

# 결과 출력
print(locations)


locations["distance_from_current"] = (locations["distance_from_current"] * 1000).round(2)
locations["distance_from_current"] = locations["distance_from_current"].astype(str) + " m"

print(locations)

locations.to_csv("updated_file.csv", index=False)