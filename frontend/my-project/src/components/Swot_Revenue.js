import React from 'react';
import './Swot_Revenue.css';
import { useNavigate } from 'react-router-dom';


const SwotRevenue = () => {
    const navigate = useNavigate();

  return (
    <div className="revenue-container">
        {/* Toggle 버튼 영역 */}
      <div className="toggle-buttons">
        <button
          className="toggle-button"
          onClick={() => navigate('/main/Swot/Performance')}
        >
          채널 성과
        </button>
        <button
          className="toggle-button"
          onClick={() => navigate('/main/Swot/Engagement')}
        >
          시청자 참여도
        </button>
        <button
          className="toggle-button active"
          onClick={() => navigate('/main/Swot/Revenue')}
        >
          채널 수익성
        </button>
      </div>
      <div className="grid-container">
        {/* 조회수 수입 및 후원 수입 */}
        <div className="section">
          <h3>조회수 수입 및 후원 수입</h3>
          {/* 내용 추가 예정 */}
        </div>

        {/* 가장 성적이 좋은 광고영상과 가장 성적이 안 좋은 광고영상 */}
        <div className="section">
          <h3>가장 성적이 좋은 광고영상과 가장 성적이 안 좋은 광고영상</h3>
          {/* 내용 추가 예정 */}
        </div>

        {/* 광고영상과 일반영상의 성과 비교 */}
        <div className="section">
          <h3>광고영상과 일반영상의 성과 비교</h3>
          {/* 내용 추가 예정 */}
        </div>

        {/* 채널의 수익성에 대한 분석결과 */}
        <div className="section">
          <h3>채널의 수익성에 대한 분석결과</h3>
          {/* 내용 추가 예정 */}
        </div>
      </div>
    </div>
  );
};

export default SwotRevenue;
