import React, { useEffect, useRef } from "react";
import './Swot_Performance.css';
import Chart from "chart.js/auto";
import { useNavigate } from 'react-router-dom';
import performanceData from '../data/performance_data.json';


const Performance = () => {
  const navigate = useNavigate();
  const barChartRef = useRef(null);
  const growthChartRef = useRef(null);
  const viewsChartRef = useRef(null);
  const uploadCycleChartRef = useRef(null);
  const activationChartRef = useRef(null);

  const barChartInstance = useRef(null);
  const growthChartInstance = useRef(null);
  const viewsChartInstance = useRef(null);
  const uploadCycleChartInstance = useRef(null);
  const activationChartInstance = useRef(null);

  useEffect(() => {
    if (!barChartRef.current) return;

    if (barChartInstance.current) {
      barChartInstance.current.destroy();
    }

    const ctx = barChartRef.current.getContext("2d");

    barChartInstance.current = new Chart(ctx, {
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
          legend: { display: false }, // 범례 제거
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
              font: { size: 12 }, // X축 폰트 크기
            },
          },
          y: {
            grid: { display: false }, // Y축 그리드 숨기기
            ticks: {
              font: { size: 12 }, // Y축 폰트 크기
            },
          },
        },
      },
    });

    return () => {
      if (barChartInstance.current) {
        barChartInstance.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (!growthChartRef.current) return;

    if (growthChartInstance.current) {
      growthChartInstance.current.destroy();
    }

    const ctx = growthChartRef.current.getContext("2d");
    growthChartInstance.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: Object.keys(performanceData.channel_growth || {}),
        datasets: [
          {
            label: "채널 성장 추세",
            data: Object.values(performanceData.channel_growth || {}),
            borderColor: "#4caf50",
            backgroundColor: "rgba(76, 175, 80, 0.2)",
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
      },
    });

    return () => {
      if (growthChartInstance.current) {
        growthChartInstance.current.destroy();
      }
    };
  }, []);

  // ✅ 조회수 변화 그래프 (Line Chart)
  useEffect(() => {
    if (!viewsChartRef.current) return;

    if (viewsChartInstance.current) {
      viewsChartInstance.current.destroy();
    }

    const ctx = viewsChartRef.current.getContext("2d");
    viewsChartInstance.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: Object.keys(performanceData.video_views || {}),
        datasets: [
          {
            label: "조회수 변화 추세",
            data: Object.values(performanceData.video_views || {}),
            borderColor: "#f44336",
            backgroundColor: "rgba(244, 67, 54, 0.2)",
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
      },
    });

    return () => {
      if (viewsChartInstance.current) {
        viewsChartInstance.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    // ✅ 업로드 주기 차트 생성
    if (!uploadCycleChartRef.current) return;
  
    if (uploadCycleChartInstance.current) {
      uploadCycleChartInstance.current.destroy();
    }
  
    const uploadCtx = uploadCycleChartRef.current.getContext("2d");
    uploadCycleChartInstance.current = new Chart(uploadCtx, {
      type: "bar",
      data: {
        labels: ["2024-01", "2024-02", "2024-03", "2024-04"],
        datasets: [
          {
            label: "업로드 영상 수",
            data: [10, 8, 12, 5],
            backgroundColor: "#4285F4",
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
      },
    });
  
    // ✅ 유사 채널 대비 활성도 차트 생성
    if (!activationChartRef.current) return;
  
    if (activationChartInstance.current) {
      activationChartInstance.current.destroy();
    }
  
    const activationCtx = activationChartRef.current.getContext("2d");
    activationChartInstance.current = new Chart(activationCtx, {
      type: "doughnut",
      data: {
        labels: ["구독자 비율", "비구독자 비율"],
        datasets: [
          {
            label: "활성도",
            data: [60, 40],
            backgroundColor: ["#4caf50", "#f44336"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
      },
    });
  
    // ✅ Cleanup 함수 추가 (차트 제거)
    return () => {
      if (uploadCycleChartInstance.current) {
        uploadCycleChartInstance.current.destroy();
      }
      if (activationChartInstance.current) {
        activationChartInstance.current.destroy();
      }
    };
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
          <canvas ref={barChartRef} width="400" height="200"></canvas>
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
        <div className="graph-card">
    <h3>채널 성장 추세</h3>
    <canvas ref={growthChartRef} width="400" height="200"></canvas>
  </div>

  <div className="graph-card">
    <h3>조회수 변화 그래프</h3>
    <canvas ref={viewsChartRef} width="400" height="200"></canvas>
  </div>
      </div>
    
  {/* ✅ 업로드 주기 섹션 추가 */}
  <div className="upload-cycle">
    <h3>영상 업로드 주기</h3>
    <canvas ref={uploadCycleChartRef} width="400" height="200"></canvas>
    <p>영상 업로드 주기가 불규칙적이에요. 규칙적인 업로드는 고정팬을 증가시켜 안정적인 조회수를 얻을 수 있어요.</p>
  </div>

  {/* ✅ 유사 채널 대비 활성도 섹션 추가 */}
  <div className="activation-metric">
    <h3>유사 채널 대비 활성도</h3>
    <canvas ref={activationChartRef} width="400" height="200"></canvas>
    <p>내 영상을 시청하는 사람 중 구독자의 비율이 높아요. 이는 팬덤이 어느 정도 형성되어 안정적인 채널 운영이 가능함을 의미합니다.</p>
  </div>
    </div>
  );
};

export default Performance;
