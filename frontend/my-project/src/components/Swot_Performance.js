import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from 'react-router-dom';
import Chart from "chart.js/auto";
import './Swot_Performance.css';
import axios from "axios";
// import performanceData from '../data/performance_data.json';


const Performance = () => {
  const navigate = useNavigate();
  const [channel_info, SetChannelInfo] = useState(null);
  const [video_info, setVideoInfo] = useState(null);
  const [thumbnail_info, setThumbnailInfo] = useState(null);
  const channelName = "너덜트";

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
    const uri_channel_info = `http://10.28.224.177:30635/dashboard/performance/channel-banner/${channelName}`;
    const uri_video_info = `http://10.28.224.177:30635/dashboard/performance/channel-performance/${channelName}`;
    // const uri_view_count=`http://10.28.224.177:30635/dashboard/performance/channel-viewcount/${channelName}`;
    // const uri_channel_growth=`http://10.28.224.177:30635/dashboard/performance/channel-growth/${channelName}`;
    // const uri_channel_feature=`http://10.28.224.177:30635/dashboard/performance/channel-feature/${channelName}`;
    axios
      .get(uri_channel_info)
      .then((response) => {
        SetChannelInfo(response.data[0]);
      })
      .catch((error) => console.error("Error fetching ad performance data:", error));

    axios
      .get(uri_video_info)
      .then((response) => {
        if (response.data) {
          if (response.data["많은 사랑을 받은 영상"]) {
            setVideoInfo(response.data["많은 사랑을 받은 영상"]); // ✅ "많은 사랑을 받은 영상" 데이터 저장
          }
          if (response.data["많은 사랑을 받은 썸네일"]) {
            setThumbnailInfo(response.data["많은 사랑을 받은 썸네일"]); // ✅ "많은 사랑을 받은 썸네일" 데이터 저장
          }
        }
      })
      .catch((error) => console.error("Error fetching video info:", error));


  }, [channelName]);
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
    // growthChartInstance.current = new Chart(ctx, {
    //   type: "line",
    //   data: {
    //     labels: Object.keys(performanceData.channel_growth || {}),
    //     datasets: [
    //       {
    //         label: "채널 성장 추세",
    //         data: Object.values(performanceData.channel_growth || {}),
    //         borderColor: "#4caf50",
    //         backgroundColor: "rgba(76, 175, 80, 0.2)",
    //         fill: true,
    //       },
    //     ],
    //   },
    //   options: {
    //     responsive: true,
    //     plugins: { legend: { display: false } },
    //   },
    // });

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
    // viewsChartInstance.current = new Chart(ctx, {
    //   type: "line",
    //   data: {
    //     labels: Object.keys(performanceData.video_views || {}),
    //     datasets: [
    //       {
    //         label: "조회수 변화 추세",
    //         data: Object.values(performanceData.video_views || {}),
    //         borderColor: "#f44336",
    //         backgroundColor: "rgba(244, 67, 54, 0.2)",
    //         fill: true,
    //       },
    //     ],
    //   },
    //   options: {
    //     responsive: true,
    //     plugins: { legend: { display: false } },
    //   },
    // });

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
        {channel_info ? (<div className="profile-section">
          <div className="profile-content">
            <img src={channel_info['썸네일']} alt="Channel Profile" className="profile-image" />
            <div className="profile-info">
              <h2 className="channel-name">{channel_info["채널 이름"]}</h2>
              <p className="channel-stats">구독자 {channel_info["구독자"]}, 동영상 {channel_info["동영상"]}</p>
            </div>
          </div>
        </div>) : (
          <p>Loading...</p>
        )}

        <div className="graph-section">
          <h3>채널 평균 조회수 및 경쟁 채널 평균 조회수</h3>
          <canvas ref={barChartRef} width="400" height="200"></canvas>
        </div>

        <div className="popular-videos">
          <h3>많은 사랑을 받은 영상</h3>
          <div className="video-list">
            {video_info ? (
              video_info.map((video, index) => (
                <div className="video-card" key={index}>
                  <img src={video["썸네일"]} alt={video["제목"]} className="thumbnail" />
                  <div className="video-info">
                    <p className="video-title">{video["제목"]}</p>
                    <div className="video-detail">
                      <span>조회수</span>
                      <span>{video["조회수"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>평균 조회율</span>
                      <span>{video["평균 조회율"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>댓글 참여율</span>
                      <span>{video["댓글 참여율"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>좋아요 참여율</span>
                      <span>{video["좋아요 참여율"]}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p>로딩 중...</p> // ✅ 데이터 로딩 중 표시
            )}
          </div>
        </div>

        <div className="popular-thumbnails">
          <h3>많은 사랑을 받은 썸네일</h3>
          <div className="video-list">
            {thumbnail_info ? (
              thumbnail_info.map((thumb, index) => (
                <div className="video-card" key={index}>
                  <img src={thumb["썸네일"]} alt={thumb["제목"]} className="thumbnail" />
                  <div className="video-info">
                    <p className="video-title">{thumb["제목"]}</p>
                    <div className="video-detail">
                      <span>조회수</span>
                      <span>{thumb["조회수"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>평균 조회율</span>
                      <span>{thumb["평균 조회율"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>댓글 참여율</span>
                      <span>{thumb["댓글 참여율"]}</span>
                    </div>
                    <div className="video-detail">
                      <span>좋아요 참여율</span>
                      <span>{thumb["좋아요 참여율"]}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p>로딩 중...</p> // ✅ 데이터 로딩 중 표시
            )}
          </div>
        </div>

      </div>


    </div>
  );
};

export default Performance;
