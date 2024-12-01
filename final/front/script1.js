//HTML에서 불러오는 부분
const chatBox = document.getElementById("chat-box"); //채팅 표출부분
const userInput = document.getElementById("user-input"); //텍스트 입력부분
const sendButton = document.getElementById("send-button"); //입력 버튼부분

// 메시지 추가 함수
function addMessage(sender, text) {
  const message = document.createElement("div"); //div 생성
  message.textContent = text; //div에 글 추가
  message.style.margin = "10px 0"; //글 간격 추가
  message.style.padding = "10px"; //글 안쪽 여백
  message.style.borderRadius = "5px"; //메세지 모서리 둥글게 하기

  if (sender === "user") {
    //user의 메세지 배경
    message.style.backgroundColor = "#dcf8c6"; //컬러 지정
    message.style.textAlign = "right"; //오른쪽정렬
  } else {
    //챗봇 메세지 배경
    message.style.backgroundColor = "#f1f0f0"; //컬러지정
    message.style.textAlign = "left"; //왼쪽 정렬
  }

  chatBox.appendChild(message); //입력된 메세지들 chatbox에 추가하기
  chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 자동 내리기
}

document.addEventListener("DOMContentLoaded", () => { //HTML 문서가 로드되고난 뒤 DOM이 준비되었을때 실행
                                                      //HTML 요소들이 아직 준비되지 않은 상태에서 실행되는걸 방지함
  // 메시지 추가 함수
  function addMessage(sender, text) { 
    const message = document.createElement("div");
    message.textContent = text; //div의 내용을 text로 지정
    message.classList.add("message", sender); //message와 sender 클래스 추가
    chatBox.appendChild(message);  //div의 요소(message)를 추가해 화면에 표시함 
    chatBox.scrollTop = chatBox.scrollHeight; //스크롤바를 가장 밑으로 가게 해서 새로운 message가 보일수 있게 해줌
  }

  // 이벤트 리스너 설정
  sendButton.addEventListener("click", () => { //클릭할때마다 내부 함수 실행
    const userMessage = userInput.value.trim(); //입력한 텍스트를 가져옴. trim으로 입력 앞 뒤의 공백 제거 (공백만 입력된 경우 방지)
    if (userMessage) { 
      addMessage("user", userMessage); //공백만 입력하거나 텍스트를 입력하지 않았을때 메세지 추가가 되지 않게 설정 
      addMessage("bot", "힘내...."); //챗봇의 응답 지정
      userInput.value = ""; //메세지 전송한 뒤 입력창 비우기
    }
  });

  //엔터를 눌렀을때도 클릭한것과 동일하게 실행하는 코드
  userInput.addEventListener("keydown", (event) => { //키보드 입력을 감지
    if (event.key === "Enter") { //enter 외에 다른 키는 무시
      event.preventDefault(); //enter키 기본동작(줄바꿈 등)을 제한
      sendButton.click(); //enter키를 눌렀을때 click과 동일하게 동작하게 해줌
    }
  });
});