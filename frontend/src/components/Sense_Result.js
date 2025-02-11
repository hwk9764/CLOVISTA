import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Sense_Result.css';
import Loader from './Loader'


const SenseResult = () => {
  const { title } = useParams(); // URL에서 전달받은 제목
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showExplanation, setShowExplanation] = useState({
    prob: false,
    danger: false,
    scope: false,
  });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const currentUser = JSON.parse(localStorage.getItem("currentUser")) || {};
        const user_email = currentUser.email;
        const name_temp = JSON.parse(localStorage.getItem(user_email)) || {};
        const userID = name_temp.name;

        const response = await axios.get(
          `http://10.28.224.177:30635/sensitive/result/${userID}`,
          { headers: { accept: "application/json" } }
        );

        const matchedResult = response.data.find(
          (item) => item.title === decodeURIComponent(title) && item.status === 1
        );

        console.log(matchedResult)
        if (matchedResult) {
          setResult(matchedResult);
        } else {
          setResult(null); // 해당 제목의 결과가 없을 경우
        }
      } catch (error) {
        console.error("❌ 결과 데이터를 불러오는 중 오류 발생:", error);
        setResult(null);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [title]);

  // 점수를 각도로 변환 (낮음/중간/높음)
  const calculateRotation = (score) => {
    const scoreMapping = { "낮음": -60, "중간": 0, "높음": 60 };
    return scoreMapping[score] || 0;
  };
  const toggleExplanation = (type) => {
    setShowExplanation((prev) => ({
      ...prev,
      [type]: !prev[type], // 해당 타입의 설명을 토글
    }));
  };

  if (loading) {
    return <Loader message="데이터를 불러오는 중..." />;
  }

  return (
    <div className="sense-result-container">

      {result ? (
        <>
          {/* 상단 컨테이너 */}
          <div className="sense-title-section">
            <h2>{result.title}</h2>
            <div className="sense-selected-text">
              {result.selected_text?.split("\n").map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>


          {/* 하단 컨테이너 */}
          <div className="sense-result-scores">
            {/* Prob Score */}
            <div className="sense-score-wrapper">
              <h2>발생 가능성</h2>
              <div className="sense-exclamation-wrapper">
                <img
                  src="/exclamation.png"
                  alt="exclamation"
                  className="sense-exclamation"
                />
                <div className="sense-explanation-hover">
                  이 지표는 텍스트가 논란으로 발전할 가능성을 측정합니다.
                </div>
              </div>
              <div className="sense-gauge">
                <div className="sense-gauge-background"></div>
                <div
                  className="sense-gauge-arrow"
                  style={{
                    transform: `rotate(${calculateRotation(result.prob_score)}deg)`,
                  }}
                ></div>
                <div className="sense-gauge-cover">
                  <span>{result.prob_score}</span>
                </div>
              </div>
              <p className="sense-score-text">  {result.prob_text.split("\n").map((line, index) => (
                <span key={index}>
                  {line}
                  <br /> {/* 줄바꿈 */}
                  <br /> {/* 줄바꿈 */}
                </span>
              ))}</p>
            </div>


            {/* Danger Score */}
            <div className="sense-score-wrapper">
              <h2>심각성</h2>
              <div className="sense-exclamation-wrapper">
                <img
                  src="/exclamation.png"
                  alt="exclamation"
                  className="sense-exclamation"
                />
                <div className="sense-explanation-hover">
                  논란 발생 시 사회적,경제적, 법적 영향의 심각성을 측정합니다.
                </div>
              </div>
              <div className="sense-gauge">
                <div className='sense-gauge-background'></div>
                <div
                  className="sense-gauge-arrow"
                  style={{
                    transform: `rotate(${calculateRotation(result.danger_score)}deg)`,
                  }}
                ></div>
                <div className="sense-gauge-cover">
                  <span>{result.danger_score}</span>
                </div>
              </div>
              <p className="sense-score-text">  {result.danger_text.split("\n").map((line, index) => (
                <span key={index}>
                  {line}
                  <br /> {/* 줄바꿈 */}
                  <br /> {/* 줄바꿈 */}
                </span>
              ))}</p>
            </div>

          </div>
        </>
      ) : (
        <p>❌ 해당 영상에 대한 분석 결과를 찾을 수 없습니다.</p>
      )}
    </div>
  );
};

export default SenseResult;
