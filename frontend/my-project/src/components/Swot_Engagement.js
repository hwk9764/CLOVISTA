import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Bar, Doughnut } from 'react-chartjs-2';
import GaugeChart from './GaugeChart.js';
import './Swot_Engagement.css';
import axios from "axios";

const SwotEngagement = () => {
  const navigate = useNavigate();

  // 막대 그래프 데이터 (경쟁 채널과 비교한 최근 30일 라이브 수)
  const liveComparisonData = {
    labels: ['내 채널', '경쟁 채널'],
    datasets: [
      {
        label: '라이브 방송 수',
        data: [13, 5], // 예제 데이터 (내 채널 13개, 경쟁 채널 5개)
        backgroundColor: ['#F0AD4E', '#5CB85C'],
      },
    ],
  };

  const videoTypeData = {
    labels: ['일반 영상', '광고 영상'],
    datasets: [
      {
        data: [70, 30], // 예제 데이터 (일반 영상 70%, 광고 영상 30%)
        backgroundColor: ['#5CB85C', '#F0AD4E'],
      },
    ],
  };

  // 막대 그래프 옵션
  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: { beginAtZero: true },
    },
  };

  // 도넛 그래프 데이터 (타겟 시청자 특성)
  const audienceData = {
    labels: ['남성', '여성'],
    datasets: [
      {
        data: [65, 35], // 예제 데이터 (남성 65%, 여성 35%)
        backgroundColor: ['#5BC0DE', '#F7A8B8'],
      },
    ],
  };

  const ageData = {
    labels: ['10대', '20대', '30대', '40대', '50대 이상'],
    datasets: [
      {
        data: [30, 40, 15, 10, 5], // 예제 데이터
        backgroundColor: ['#5BC0DE', '#F0AD4E', '#5CB85C', '#D9534F', '#777'],
      },
    ],
  };

  // 최근 영상 키워드
  const recentKeywords = ['운동', '크리에이터', '챌린지', '노래 추천', '트렌드'];

  return (
    <div className="engagement-container">
      {/* Toggle 버튼 영역 */}
      <div className="toggle-buttons">
        <button className="toggle-button" onClick={() => navigate('/main/Swot/Performance')}>
          채널 성과
        </button>
        <button className="toggle-button active" onClick={() => navigate('/main/Swot/Engagement')}>
          시청자 참여도
        </button>
        <button className="toggle-button" onClick={() => navigate('/main/Swot/Revenue')}>
          채널 수익성
        </button>
      </div>

      <div className="grid-container">
        {/* 시청자의 채널 참여도 */}
        <div className="section">
          <h2 className="section-title">시청자의 채널 참여도</h2>
          <div className="gauge-container">
            <GaugeChart label="좋아요 비율" value={0.11} color="#D9534F" />
            <GaugeChart label="댓글 비율" value={0.0369} color="#F0AD4E" />
            <GaugeChart label="공유 비율" value={0.0587} color="#5CB85C" />
          </div>
        </div>

        {/* 크리에이터의 소통 활동 */}
        <div className="section">
          <h2 className="section-title">크리에이터의 소통 활동</h2>
          <div className="chart-container">
            {/* 막대 그래프 - 최근 30일 라이브 수 */}
            <div className="bar-chart">
              <h3>경쟁 채널과 비교한 최근 30일 라이브 수</h3>
              <Bar data={liveComparisonData} options={barOptions} />
            </div>

            {/* 도넛 게이지 그래프 - 라이브 평균 시청자 수 */}
            <div className="gauge-chart">
              <h3>라이브 평균 시청자 수</h3>
              <GaugeChart label="라이브 평균 시청자 수" value={315100 / 5000} color="#5CB85C" />
            </div>
          </div>
        </div>

        {/* 시청자 타겟팅 전략 */}
        <div className="section">
          <h2 className="section-title">시청자 타겟팅 전략</h2>
          <div className="target-audience-container">
            {/* 타겟 시청자 특성 */}
            <div className="doughnut-chart">
              <h3>타겟 시청자 특성</h3>
              <Doughnut data={audienceData} />
            </div>
            <div className="doughnut-chart">
              <h3>연령별 분포</h3>
              <Doughnut data={ageData} />
            </div>
          </div>

          {/* 최근 영상 키워드 */}
          <div className="keywords-container">
            <h3>최근 영상 키워드</h3>
            <div className="keyword-tags">
              {recentKeywords.map((keyword, index) => (
                <span key={index} className="keyword-tag">{keyword}</span>
              ))}
            </div>
          </div>
        </div>

        {/* 업로드 시간대 비교 */}
        <div className="section">
          <h2 className="section-title">업로드 시간대 비교</h2>
          <div className="upload-time-container">
            {/* 업로드 시간 & 시청 시간 텍스트 출력 */}
            <div className="upload-time-text">
              <h3>영상 업로드 시간</h3>
              <p>오후 12시 ~ 3시</p>
              <h3>주요 시청 시간</h3>
              <p>오후 3시 ~ 6시</p>
            </div>

            {/* 일반 영상 vs 광고 영상 비율 */}
            <div className="doughnut-chart">
              <h3>일반 / 광고 영상 비율</h3>
              <Doughnut data={videoTypeData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SwotEngagement;
