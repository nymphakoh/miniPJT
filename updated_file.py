import requests
from bs4 import BeautifulSoup
import pandas as pd 
import pymysql
import time

# MySQL 연결 설정
def connect_to_mysql():
    return pymysql.connect(
        host="localhost",       # MySQL 호스트 (예: "127.0.0.1")
        user="root",            # MySQL 사용자
        password="1234",  # MySQL 비밀번호
        database="updated_file", # 사용할 데이터베이스
        charset="utf8mb4"       # 한글 지원
    )

'''# CSV 데이터를 MySQL에 삽입
def csv_to_mysql(csv_file_path, table_name):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)

    # MySQL 연결
    connection = connect_to_mysql()
    cursor = connection.cursor()

    try:
        # 데이터 삽입 쿼리
        for _, row in df.iterrows():
            sql = f"""
            INSERT INTO {table_name} ({', '.join(df.columns)})
            VALUES ({', '.join(['%s'] * len(row))})
            """
            cursor.execute(sql, tuple(row))

        # 변경 사항 저장
        connection.commit()
        print("CSV 데이터를 성공적으로 MySQL에 업로드했습니다.")

    except pymysql.MySQLError as e:
        print(f"MySQL 에러: {e}")
    finally:
        # 연결 닫기
        cursor.close()
        connection.close()

# 메인 코드
if __name__ == "__main__":
    updated_file_path = "updated_file.csv"  # CSV 파일 경로
    updated_file = "updated_file"  # 삽입할 MySQL 테이블 이름

    # CSV 데이터를 MySQL로 업로드
    csv_to_mysql(updated_file_path, updated_file)'''


# SQL 쿼리 결과를 Pandas DataFrame으로 가져오기
def fetch_data():
    connection = connect_to_mysql()  # MySQL 연결
    try:
        query = "SELECT * FROM chart;"  # 원하는 SQL 쿼리
        df = pd.read_sql(query, connection)  # Pandas로 결과 가져오기
        return df
    except pymysql.MySQLError as e:
        print(f"Error fetching data from MySQL: {e}")
        return None
    finally:
        connection.close()  # 연결 닫기

# 데이터를 가져와서 출력
df = fetch_data()
if df is not None:
    print(df.head())  # DataFrame의 앞부분 출력
else:
    print("No data fetched.")   




