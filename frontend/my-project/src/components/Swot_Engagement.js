import React from 'react';
import { useNavigate } from 'react-router-dom'; // ✅ navigate 추가
import './Swot_Engagement.css';
import GaugeChart from './GaugeChart.js'

const SwotEngagement = () => {  // ✅ 컴포넌트 정의 추가
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
          className="toggle-button active"
          onClick={() => navigate('/main/Swot/Engagement')}
        >
          시청자 참여도
        </button>
        <button
          className="toggle-button"
          onClick={() => navigate('/main/Swot/Revenue')}
        >
          채널 수익성
        </button>
      </div>

      <div className="grid-container">
        {/* 시청자의 채널 참여도 */}
        <div className="section">
          <h3>추후 시청자 참여도 페이지</h3>
          <div className="engagement-container">
        <h2 className="section-title">시청자의 채널 참여도</h2>
        <div className="gauge-container">
          <GaugeChart label="좋아요 비율" value={0.11} color="#D9534F" />
          <GaugeChart label="댓글 비율" value={3.69} color="#F0AD4E" />
          <GaugeChart label="공유 비율" value={5.87} color="#5CB85C" />
      </div>
    </div>
        </div>

        {/* 크리에이터의 소통 활동 */}
        <div className="section">
          <h3>작업 아직 안함</h3>
          {/* 내용 추가 예정 */}
        </div>

        {/* 시청자 타겟팅 전략 */}
        <div className="section">
          <h3>나중에 수정해야 됨</h3>
          {/* 내용 추가 예정 */}
        </div>

        {/* 업로드 시간대 비교교 */}
        <div className="section">
          <h3>ㅋㅋ루 삥뽕</h3>
          {/* 내용 추가 예정 */}
        </div>
      </div>
    </div>
  );
};

export default SwotEngagement;
