import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Identity.css";

const Identity = () => {
  const [surveyCompleted, setSurveyCompleted] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const responses = JSON.parse(localStorage.getItem("identitySurveyResponses"));
    setSurveyCompleted(!!responses); // identitySurveyResponses가 있으면 true, 없으면 false
  }, []);

  return (
    <div className="identity-container">
      {/* 설문조사 다시하기 버튼 */}
      <button className="retry-button" onClick={() => navigate("/main/identity/survey")}>
        설문조사 다시하기
      </button>

      <div className="identity-result">
        {/* 설문조사 안 했으면 블러 처리된 오버레이 추가 */}
        {!surveyCompleted && (
          <div className="overlay">
            <p>정체성 파악을 위한 설문조사를 진행해주세요.</p>
            <button onClick={() => navigate("/main/identity/survey")}>설문조사 하러가기</button>
          </div>
        )}
        <h2>정체성 평가 결과</h2>
        <p>여기에 정체성 분석 결과 내용을 입력하세요. 여러 줄의 텍스트가 표시될 수 있습니다.</p>
      </div>

      <div className="recommendations">
        <div className="recommend-box">추천 콘텐츠 1<br />자세한 추천 내용이 들어갑니다.</div>
        <div className="recommend-box">추천 콘텐츠 2<br />관련된 설명을 추가할 수 있습니다.</div>
        <div className="recommend-box">추천 콘텐츠 3<br />더 많은 정보를 입력해도 문제없습니다.</div>
      </div>
    </div>
  );
};

export default Identity;
