import pandas as pd
import os
from openai import OpenAI
import numpy as np
import faiss

# CSV 파일 경로
csv_path = '/Users/jejinan/Desktop/sesac/realdata/zeropay_dobong_rev3.csv'

# CSV 파일 읽기
df = pd.read_csv(csv_path, encoding='utf-8-sig')
df['combined_text'] = df[df.columns.values].astype(str).agg(' | '.join, axis=1)


client = OpenAI(api_key =os.getenv("API_KEY"))

# FAISS 인덱스 로드
index = faiss.read_index("faiss_index.idx")
print("FAISS 인덱스가 'faiss_index.idx' 파일에서 로드되었습니다.")
print(f"FAISS에 저장된 벡터 수: {index.ntotal}")

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# 사용자 질의
query_text = ("오늘은 중국집 먹고싶어")

# 질의 임베딩 생성
query_embedding = get_embedding(query_text)
query_vector = np.array([query_embedding]).astype('float32')

# 유사한 상위 5개 결과 검색
k = 15
distances, indices = index.search(query_vector, k)

# 검색 결과 출력
for i in range(k):
    idx = indices[0][i]
    distance = distances[0][i]
    recommended_restaurant = df.iloc[idx]
    print(recommended_restaurant)

# 검색된 텍스트 수집
relevant_texts = df.iloc[indices[0]]['combined_text'].tolist()

# 프롬프트 작성
context = "\n".join(relevant_texts)
prompt = f"""
다음은 사용자 질문 : {query_text} 에 대한 식당정보입니다. :
창동씨드큐브를 기준 거리(미터), 지정등급은 위생등급
{context}

이 정보를 바탕으로 사용자에게 질문에 맞는 장소를 추천해주세요. 가게이름을 기반으로 검색해서 리뷰 제공
"""

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 주어진 데이터에 기반하여 추천 가게를 검색해서 다양한 정보 제공을 제공하는 유용한 어시스턴트입니다."},
        {
            "role": "user","content": prompt
        }
    ],
    max_tokens= 3000
)

# 응답 출력
print(completion.choices[0].message)
