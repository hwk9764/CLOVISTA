import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./SurveyChatbot.css";

const questions = [
  { type: "text", question: "영상 제작 분야는 무엇인가요?", examples: "예: 요리, 여행, 게임, 뷰티 등" },
  { type: "text", question: "영상 콘텐츠 유형은 어떻게 되나요?", examples: "예: 브이로그, 리뷰, 튜토리얼, 예능 등" },
  { type: "multiple_choice", question: "영상 작업 주기는 어떻게 되나요?", options: ["1달 1회", "1주일 1회", "1주일 2회", "1주일 3회", "1주일 4회", "매일"] },
  { type: "text", question: "보유하고 있는 제작용 장비가 있나요?", examples: "예: 편집 프로그램, 고프로, 캡쳐보드, 최신 스마트폰 등" },
  { type: "text", question: "평소에 생각했던 아이디어가 있나요?", examples: "예: 소개팅 상황극, 일본 여행 브이로그 등" },
  { type: "text", question: "유튜브를 운영하며 이루고 싶은 목표가 있나요?", examples: "예: 실버버튼 받기, 1년 내에 수익 창출 허가받기, 협찬 유치하기 등" }
];

const SurveyChatbot = () => {
  const [messages, setMessages] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [inputValue, setInputValue] = useState("");
  const chatEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    setMessages([{ sender: "bot", text: questions[0].question }]);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAnswer = (answer) => {
    const newMessages = [...messages, { sender: "user", text: answer }];

    if (currentQuestionIndex < questions.length - 1) {
      newMessages.push({ sender: "bot", text: questions[currentQuestionIndex + 1].question });
      setMessages(newMessages);
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // 🔹 설문 결과 저장 (identitySurveyResponses 사용)
      localStorage.setItem("identitySurveyResponses", JSON.stringify(newMessages));

      // 🔹 설문 완료 메시지 추가
      newMessages.push({ sender: "bot", text: "설문이 완료되었습니다! 감사합니다. 😊" });
      setMessages([...newMessages]);

      // 🔹 2초 후 메인 페이지로 이동
      setTimeout(() => navigate("/main/identity"), 2000);
    }

    setInputValue("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && inputValue.trim()) {
      handleAnswer(inputValue.trim());
    }
  };

  // 🔹 현재 질문 가져오기 (배열 범위를 벗어나지 않도록 체크)
  const currentQuestion = questions[currentQuestionIndex] || null;
  const placeholderText = currentQuestion?.examples || "메시지를 입력하세요...";

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-bubble ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* 🔹 질문이 존재하는 경우에만 입력창 표시 */}
      {currentQuestion ? (
        currentQuestion.type === "multiple_choice" ? (
          <div className="options">
            {currentQuestion.options.map((option, index) => (
              <button key={index} onClick={() => handleAnswer(option)}>
                {option}
              </button>
            ))}
          </div>
        ) : (
          <div className="input-area">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder={placeholderText} // 🔥 플레이스홀더 수정
            />
            <button onClick={() => handleAnswer(inputValue)}>전송</button>
          </div>
        )
      ) : null}
    </div>
  );
};

export default SurveyChatbot;
