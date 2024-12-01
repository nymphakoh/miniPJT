//HTML에서 불러오는 부분
const chatBox = document.getElementById("chat-box"); //채팅 표출부분
const userInput = document.getElementById("user-input"); //텍스트 입력부분
const sendButton = document.getElementById("send-button"); //입력 버튼부분

// 메시지 추가 함수
function addMessage(sender, text) {
  const message = document.createElement("div"); //div 생성
  message.textContent = text; //글 추가
  message.style.margin = "10px 0"; //위아래 간격
  message.style.padding = "10px"; //안쪽 여백
  message.style.borderRadius = "5px";
  message.style.maxWidth = "80%";

  if (sender === "user") {
    message.style.backgroundColor = "#dcf8c6";
    message.style.textAlign = "right";
    message.style.marginLeft = "20%";
  } else {
    message.style.backgroundColor = "#f1f0f0";
    message.style.textAlign = "left";
    message.style.marginRight = "20%";
  }

  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 자동 내리기
}

// 비동기 함수로 백엔드 API 호출
async function sendMessage(message) {
  console.log("sendMessage 함수 호출됨:", message); // 로그 추가
  try {
    const response = await fetch('http://localhost:5001/chat', { // 백엔드 서버 주소'http://localhost:5001/chat'
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: message })
    });

    console.log("fetch 응답 상태:", response.status); // 응답 상태 로그

    if (!response.ok) {
      throw new Error('네트워크 응답에 문제가 있습니다.');
    }

    const data = await response.json();
    console.log("fetch 응답 데이터:", data); // 응답 데이터 로그
    if (data.error) {
      addMessage("bot", "죄송합니다. 오류가 발생했습니다.");
    } else {
      addMessage("bot", data.response);
    }
  } catch (error) {
    console.error('오류 발생:', error);
    addMessage("bot", "죄송합니다. 요청을 처리하는 중 오류가 발생했습니다.");
  }
}

// 메시지 전송 로직을 함수로 분리
function sendUserMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage) {
    addMessage("user", userMessage); // 메시지 추가
    sendMessage(userMessage); // 백엔드로 메시지 전송
    userInput.value = ""; // 입력창 비우기
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  // 버튼 클릭 동작 정의
  sendButton.addEventListener("click", () => {
    sendUserMessage();
  });

  // 엔터 키를 눌렀을 때 메시지 전송 함수 호출
  userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); // 기본 동작(폼 제출 등) 방지
      sendUserMessage();
    }
  });
});