import os
from openai import OpenAI
import pandas as pd
import faiss
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Flask 앱 초기화
app = Flask(__name__)
#CORS(app)  # 모든 도메인에 대해 CORS 허용. 필요에 따라 설정 조정 가능
CORS(app, resources={
    r"/chat": {"origins": "*"},
    r"/hello": {"origins": "*"}
})

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # 로깅 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),  # 콘솔에 로그 출력
        logging.FileHandler("app.log", encoding='utf-8')  # 로그 파일에 기록

    ]
)

logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info(f"Received {request.method} request for {request.url}")
    logger.debug(f"Request headers: {request.headers}")
    logger.debug(f"Request body: {request.get_data()}")

@app.after_request
def log_response_info(response):
    logger.info(f"Responding with status {response.status}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response body: {response.get_data()}")
    return response


# CSV 파일 경로
csv_path = 'zeropay_dobong_rev3.csv'

# CSV 파일 읽기
df = pd.read_csv(csv_path, encoding='utf-8-sig')
df['combined_text'] = df[df.columns.values].astype(str).agg(' | '.join, axis=1)

openai_api_key = os.getenv("API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
client = OpenAI(api_key=openai_api_key)

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


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    #user_message = "점심 추천해줘"
    if not user_message:
        return jsonify({"error": "No message provided."}), 400# 사용자 질의

    try:
        # 질의 임베딩 생성
        query_embedding = get_embedding(user_message)
        query_vector = np.array([query_embedding]).astype('float32')

        # 유사한 상위 5개 결과 검색
        k = 7
        distances, indices = index.search(query_vector, k)

        # 검색 결과 출력
        # for i in range(k):
        #     idx = indices[0][i]
        #     distance = distances[0][i]
        #     recommended_restaurant = df.iloc[idx]
        #     print(recommended_restaurant)

        # 검색된 텍스트 수집
        relevant_texts = df.iloc[indices[0]]['combined_text'].tolist()

        # 프롬프트 작성
        context = "\n".join(relevant_texts)
        prompt = f"""
        다음은 사용자 질문 : {user_message} 에 대한 식당정보입니다. :
        창동씨드큐브를 기준 거리(미터), 지정등급은 위생등급
        {context}
        
        이 정보를 바탕으로 사용자에게 질문에 맞는 장소를 추천해주세요. 가게이름을 기반으로 검색해서 리뷰 제공
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
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
        response = completion.choices[0].message.content

        return jsonify({"response": response})

    except Exception as e:
        print(f"오류 발생: {e}")
        logger.error("An error occurred", exc_info=True)
        return jsonify({"error": "An error occurred while processing your request."}), 500


#chat()
#서버 실행 backend 에서 python app.py 종료 Ctrl + C
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
