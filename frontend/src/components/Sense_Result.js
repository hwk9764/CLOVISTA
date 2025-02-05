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
        const userData = JSON.parse(localStorage.getItem("user") || "{}");
        const userID = encodeURIComponent(userData.name || "unknown");

        const response = await axios.get(
          `http://10.28.224.177:30635/sensitive/result/${userID}`,
          { headers: { accept: "application/json" } }
        );

        const matchedResult = response.data.find(
          (item) => item.title === decodeURIComponent(title) && item.status === 1
        );

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
          <div className="sense-result-header">
            <div className="sense-title-section">
              <h2>{result.title}</h2>
              <div className="sense-selected-text">
                {result.selected_text?.split("\n").map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
                {/* 엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트
                엄청 긴 텍스트 테스트 */}
              </div>
            </div>
            <div className='sense-similar-case-card'>
              <h2>유사한 과거<br />논란 사례 분석</h2>
              <img src={'/similar_case_icon.png'} alt="similar_case_pic" className='sense-similar-case-icon' />
              <p>스크립트를 분석하여 식별된 잠재 논란 요소 중, 과거에 일었던 논란과 유사할 수 있는 사례를 살펴봅니다.</p>
              <button
                className="sense-similar-cases-button"
                onClick={() => navigate('/main/similar-cases')}
              >
                보러 가기
              </button>
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
              <p className="sense-score-text">{result.prob_text}</p>
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
              <p className="sense-score-text">{result.danger_text}</p>
            </div>

            {/* Scope Score */}
            <div className="sense-score-wrapper">
              <h2>영향 범위</h2>
              <div className="sense-exclamation-wrapper">
                <img
                  src="/exclamation.png"
                  alt="exclamation"
                  className="sense-exclamation"
                />
                <div className="sense-explanation-hover">
                  논란이 영향을 미칠 대상과 <br/>범위를 측정합니다.
                </div>
              </div>
              <div className="sense-gauge">
                <div className='sense-gauge-background'></div>
                <div
                  className="sense-gauge-arrow"
                  style={{
                    transform: `rotate(${calculateRotation(result.scope_score)}deg)`,
                  }}
                ></div>
                <div className="sense-gauge-cover">
                  <span>{result.scope_score}</span>
                </div>
              </div>
              <p className="sense-score-text">{result.scope_text}</p>
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
