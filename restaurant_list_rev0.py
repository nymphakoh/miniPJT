import pandas as pd

# CSV 파일 읽기
file1 = pd.read_csv('C:\\Users\\r2com\\Documents\\Selenium_test\\mini PJT\\restaurants_cafes_info_sig.csv', encoding='utf-8')
file2 = pd.read_csv('C:\\Users\\r2com\\Documents\\Selenium_test\\mini PJT\\sanitation.csv', encoding='Cp949')



# 데이터 전처리: 문자열 변환 및 결측치 처리
file1['place_name'] = file1['place_name'].astype(str).fillna('')
file1['road_address_name'] = file1['road_address_name'].astype(str).fillna('')

file2['업소명'] = file2['업소명'].astype(str).fillna('')
file2['소재지'] = file2['소재지'].astype(str).fillna('')

# 'place_name' 앞 2글자를 추출하여 새로운 열 생성
file1['place_name_prefix'] = file1['place_name'].str[:2]

# 병합 결과를 저장할 리스트 초기화
merged_rows = []
#isMatch = False
# file1의 각 행에 대해 처리
for idx, row in file1.iterrows():
    merged = False #병합 여부 확인을 위한 플래그
    for j, row2 in file2.iterrows():
    #print(idx,row)
    #조건에 맞는 file2의 행 필터링
      if (row['road_address_name'] in row2['소재지']) and (row['place_name_prefix'] in row2['업소명']):
            # 조건에 맞는 첫 번째 행과 병합
            merged_row = pd.concat([row, row2], axis=0)
            merged_rows.append(merged_row)
            merged = True
            break  # 조건에 맞는 행을 찾으면 내부 루프 종료
    '''condition = (
            row2['소재지'].str.contains(row['road_address_name'], na=False, regex=False) &
            row2['업소명'].str.contains(row['place_name_prefix'], na=False, regex=False)
        )
    #print(file2['소재지'].str.contains(row['road_address_name']))
    # print('소재지', file2['소재지'].str.contains(row['road_address_name'], na=False, regex=False))
        #matched = file2[condition]
    # print(matched)#'''
    
    if not merged : 
            # 조건에 맞는 첫 번째 행과 병합
            #merged_row = pd.concat([row, matched.iloc[0]], axis=1)
            #break
        merged_rows.append(row)

        #else:
        # 조건에 맞는 행이 없으면 file1의 행만 사용
    '''merged_row = row
        merged_rows.append(merged_row)'''

# 병합된 데이터프레임 생성
result = pd.DataFrame(merged_rows)
print(len(result))

# 불필요한 열 제거 (필요에 따라 수정)
#result = result.drop(columns=['place_name_prefix'])

# 결과를 CSV 파일로 저장
result.to_csv('merged_file_rev0.csv', index=False)
