'''input_file = "C:\\Users\\r2com\\Documents\\Selenium_test\\mini PJT\\sanitation.csv"  # 한글 인코딩된 원본 파일
output_file = "C:\\Users\\r2com\\Documents\\Selenium_test\\mini PJT\\rsanitation_utf8.csv"  # UTF-8로 변환된 파일


# import chardet

# with open(input_file, 'rb') as f:
#     rawdata = f.read()
#     result = chardet.detect(rawdata)
#     print(result)  # {'encoding': 'utf-8', 'confidence': 0.99}

#파일 변환
with open(input_file, "r", encoding="GB2312") as infile:
    content = infile.read()  # 파일 읽기

#UTF-8로 저장
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write(content)

print("파일이 UTF-8 형식으로 저장되었습니다:", output_file)'''


import pandas as pd

# CSV 파일 불러오기
#df1 = pd.read_csv('sanitation.csv')  # 첫 번째 CSV 파일
path = 'C:\\Users\\r2com\\Documents\\Selenium_test\\mini PJT\\'


df1 = pd.read_csv(path + 'sanitation.csv', encoding='Cp949', header=0)
df2 = pd.read_csv(path + 'restaurants_cafes_info_sig.csv')  # 두 번째 CSV 파일

'''print(df.head())  # 첫 번째 데이터프레임 미리보기
print(df2.head())  # 두 번째 데이터프레임 미리보기'''

# 열 이름 확인
print("첫 번째 파일 열 이름:", df1.columns)
print("두 번째 파일 열 이름:", df2.columns)

# # 열 이름 수정 (필요할 경우)
df1.rename(columns={'업소명': '식당이름'}, inplace=True)
df2.rename(columns={'place_name': '식당이름'}, inplace=True)

# # 공백 제거
# df1.columns = df1.columns.str.strip()
# df2.columns = df2.columns.str.strip()

# # 공통 열인 '식당이름'을 기준으로 병합
# merged_df = pd.merge(df1, df2, on='식당이름', how='inner')

# # 병합 결과 저장
# merged_df.to_csv('merged_data.csv', index=False, encoding='utf-8-sig')

# print("병합 완료! 결과가 'merged_data.csv'에 저장되었습니다.")

# import os
# print(os.getcwd()) 

merged_rev0 = pd.merge(df1, df2, on= '식당이름' )
merged_rev0.to_csv('merged_data.csv', index=False, encoding='utf-8')

print("병합 완료! 결과가 'merged_data.csv'에 저장되었습니다.")
