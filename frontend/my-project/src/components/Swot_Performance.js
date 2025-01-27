import React, { useEffect, useRef } from "react";
import './Swot_Performance.css';
import Chart from "chart.js/auto";
import { useNavigate } from 'react-router-dom';


const Performance = () => {
  const navigate = useNavigate();
  const chartRef = useRef(null);

  useEffect(() => {
    const ctx = chartRef.current.getContext("2d");

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["내 채널 평균 조회수", "경쟁 채널 평균 조회수"], // Y축 레이블
        datasets: [
          {
            label: "평균 조회수",
            data: [100921304, 50921214], // 데이터 값
            backgroundColor: ["#c8f5a8", "#f5d6a8"], // 각 막대 색상
            borderRadius: 5, // 막대 테두리 둥글게
          },
        ],
      },
      options: {
        indexAxis: "y", // 그래프를 가로로 눕힘
        responsive: true,
        plugins: {
          legend: {
            display: false, // 범례 제거
          },
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                return tooltipItem.raw.toLocaleString() + "회"; // 숫자 포맷
              },
            },
          },
        },
        scales: {
          x: {
            ticks: {
              callback: (value) => value.toLocaleString() + "회", // X축 숫자 포맷
              font: {
                size: 12, // X축 폰트 크기
              },
            },
          },
          y: {
            grid: {
              display: false, // Y축 그리드 숨기기
            },
            ticks: {
              font: {
                size: 12, // Y축 폰트 크기
              },
            },
          },
        },
      },
    });
  }, []);
  return (
    <div className="performance-container">
      {/* Toggle 버튼 영역 */}
      <div className="toggle-buttons">
        <button
          className="toggle-button active"
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
          className="toggle-button"
          onClick={() => navigate('/main/Swot/Revenue')}
        >
          채널 수익성
        </button>
      </div>

      <div className="grid-container">
        <div className="profile-section">
          <div className="profile-content">
            <img src="/channel_image.png" alt="Channel Profile" className="profile-image" />
            <div className="profile-info">
              <h2 className="channel-name">빠더너스 BDNS</h2>
              <p className="channel-stats">구독자 178만명, 동영상 1.2천개</p>
            </div>
          </div>
        </div>

        <div className="graph-section">
          <h3>채널 평균 조회수 및 경쟁 채널 평균 조회수</h3>
          <canvas ref={chartRef} width="400" height="200"></canvas>
        </div>

        <div className="popular-videos">
          <h3>많은 사랑을 받은 영상</h3>
          <div className="video-list">
            {[1,2,3].map(index => (
              <div className="video-card" key={index}>
              <img src="/example_thumbnail_2.png" alt="Thumbnail" className="thumbnail" />
              <div className="video-info">
                <p className="video-title">영상 제목 {index}</p>
                <div className="video-detail">
                  <span>조회수</span>
                  <span>14k</span>
                </div>
                <div className="video-detail">
                  <span>평균 조회율</span>
                  <span>15%</span>
                </div>
                <div className="video-detail">
                  <span>댓글 참여율</span>
                  <span>1.3%</span>
                </div>
                <div className="video-detail">
                  <span>좋아요 참여율</span>
                  <span>2.4%</span>
                </div>
              </div>
            </div>
            ))}
          </div>
        </div>

        <div className="popular-thumbnails">
          <h3>많은 사랑을 받은 썸네일</h3>
          <div className="video-list">
            {[1,2,3].map(index => (
              <div className="video-card" key={index}>
              <img src="/example_thumbnail_2.png" alt="Thumbnail" className="thumbnail" />
              <div className="video-info">
                <p className="video-title">영상 제목 {index}</p>
                <div className="video-detail">
                  <span>조회수</span>
                  <span>14k</span>
                </div>
                <div className="video-detail">
                  <span>평균 조회율</span>
                  <span>15%</span>
                </div>
                <div className="video-detail">
                  <span>댓글 참여율</span>
                  <span>1.3%</span>
                </div>
                <div className="video-detail">
                  <span>좋아요 참여율</span>
                  <span>2.4%</span>
                </div>
              </div>
            </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Performance;
