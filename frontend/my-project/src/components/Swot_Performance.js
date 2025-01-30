import React, { useEffect, useRef, useState } from "react";
import { data, useNavigate } from 'react-router-dom';
import Chart from "chart.js/auto";
import './Swot_Performance.css';
import axios from "axios";


const Performance = () => {
  const navigate = useNavigate();
  const [channel_info, SetChannelInfo] = useState(null);
  const [video_info, setVideoInfo] = useState(null);
  const [thumbnail_info, setThumbnailInfo] = useState(null);
  const channelName = "너덜트";

  const viewsChartRef = useRef(null);
  const growthChartRef = useRef(null);
  const viewsChangeChartRef = useRef(null);
  const uploadCycleChartRef = useRef(null);
  const activationChartRef = useRef(null);


  useEffect(() => {
    const uri_channel_info = `http://10.28.224.177:30635/dashboard/performance/channel-banner/${channelName}`;
    const uri_video_info = `http://10.28.224.177:30635/dashboard/performance/channel-performance/${channelName}`;
    const uri_view_count = `http://10.28.224.177:30635/dashboard/performance/channel-viewcount/${channelName}`;
    const uri_channel_growth = `http://10.28.224.177:30635/dashboard/performance/channel-growth/${channelName}`;
    const uri_channel_feature = `http://10.28.224.177:30635/dashboard/performance/channel-feature/${channelName}`;
    // 채널정보 가져오기
    axios
      .get(uri_channel_info)
      .then((response) => {
        SetChannelInfo(response.data[0]);
      })
      .catch((error) => console.error("Error fetching ad performance data:", error));
    // 사랑받은 영상, 썸네일 가져오기
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

    // 내 채널, 경쟁 채널 평균 조회수
    axios
      .get(uri_view_count)
      .then((response) => {
        const view_data = response.data[0]
        const user_avg_view = view_data["내 채널 평균 조회수"]
        const competitive_avg_view = view_data["경쟁 채널 평균 조회수"]
        const ctx = viewsChartRef.current.getContext("2d");
        const viewsData = {
          labels: ["내 채널", "경쟁 채널"],
          datasets: [
            {
              label: ["내 채널", "경쟁 채널"],
              data: [user_avg_view, competitive_avg_view],
              backgroundColor: ["#EDF9DE", "#FBD8A8"],
              barThickness: 40,
            },
          ],
        };
        new Chart(ctx, {
          type: "bar",
          data: viewsData,
          options: {
            indexAxis: "y",
            responsive: true,
            plugins: { legend: { display: false } },
          },
        });

      })
      .catch((error) => console.error("Error fetching views data :", error));

    // 채널 성장 추세
    axios
      .get(uri_channel_growth)
      .then((response) => {
        const view_data = response.data[0]
        const labels = view_data["x"]; // x축 (날짜)
        const subscribersData = view_data["구독자 그래프"]; // y축 (구독자 수)

        const ctx = growthChartRef.current.getContext("2d");
        const chartData = {
          labels: labels, // x축 데이터
          datasets: [
            {
              label: "구독자 수", // 라벨
              data: subscribersData, // y축 데이터
              borderColor: "#4CAF50", // 선 색상
              backgroundColor: "rgba(76, 175, 80, 0.2)", // 투명 배경
              fill: true, // 선 아래 영역 채우기
              tension: 0.4, // 곡선 정도
            },
          ],
        };
        new Chart(ctx, {
          type: "line", // 차트 타입: Line
          data: chartData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true, // 범례 표시
                position: "top",
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "날짜", // x축 제목
                },
              },
              y: {
                title: {
                  display: true,
                  text: "구독자 수", // y축 제목
                },
                beginAtZero: true, // y축 0부터 시작
              },
            },
          },
        });
      })
      .catch((error) => console.error("Error fetching growth flow data :", error));

    // 조회수 변화 그래프
    axios
      .get(uri_channel_growth)
      .then((response) => {
        const view_data = response.data[0];
        const labels = view_data["x"];
        const dailyViews = view_data["조회수 그래프"]["daily"];
        const totalViews = view_data["조회수 그래프"]["total"];
        const ctx = viewsChangeChartRef.current.getContext("2d");

        const chartData = {
          labels: labels, // x축 데이터 (날짜)
          datasets: [
            {
              type: "line", // Line Chart
              label: "일일 조회수",
              data: dailyViews,
              borderColor: "#4CAF50", // 선 색상
              backgroundColor: "rgba(76, 175, 80, 0.2)", // 투명 배경
              fill: true, // 선 아래 영역 채우기
              tension: 0.4, // 곡선 정도
              yAxisID: "y", // Y축 ID 설정
            },
            {
              type: "bar", // Bar Chart
              label: "누적 조회수",
              data: totalViews,
              backgroundColor: "rgba(255, 159, 64, 0.6)", // 바 색상
              barThickness: 10, // 바 두께
              yAxisID: "y1", // 다른 Y축 ID 설정
            },
          ],
        };

        new Chart(ctx, {
          type: "bar", // 복합 차트의 기본 타입은 bar
          data: chartData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true, // 범례 표시
                position: "top",
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "날짜", // x축 제목
                },
              },
              y: {
                type: "linear", // 첫 번째 Y축
                position: "left",
                title: {
                  display: true,
                  text: "일일 조회수", // Y축 제목
                },
              },
              y1: {
                type: "linear", // 두 번째 Y축
                position: "right", // 오른쪽에 표시
                title: {
                  display: true,
                  text: "누적 조회수", // Y축 제목
                },
                grid: {
                  drawOnChartArea: false, // 격자 표시 안함
                },
              },
            },
          },
        });
      })
      .catch((error) => console.error("Error fetching growth flow data :", error));


    axios
      .get(uri_channel_feature)
      .then((response) => {
        const data = response.data[0]; // 데이터 가져오기
        const labels = data["x"]; // x축 데이터 (월)
        const videoCounts = data["영상 수"]; // y축 데이터 (영상 수)

        const ctx = uploadCycleChartRef.current.getContext("2d");

        const chartData = {
          labels: labels, // x축 데이터
          datasets: [
            {
              label: "업로드 영상 수",
              data: videoCounts, // y축 데이터
              backgroundColor: "rgba(54, 162, 235, 0.7)", // 바 색상
              borderColor: "rgba(54, 162, 235, 1)", // 경계선 색상
              borderWidth: 1, // 경계선 두께
              barThickness: 30, // 바 두께
            },
          ],
        };

        new Chart(ctx, {
          type: "bar", // 차트 타입: Bar
          data: chartData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: false, // 범례 표시 안함
              },
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return `영상 수: ${tooltipItem.raw}`; // 툴팁에 표시될 내용
                  },
                },
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "월", // x축 제목
                },
              },
              y: {
                title: {
                  display: true,
                  text: "영상 수", // y축 제목
                },
                beginAtZero: true, // y축 0부터 시작
                ticks: {
                  stepSize: 1, // y축 간격
                },
              },
            },
          },
        });
      })
      .catch((error) => console.error("Error fetching channel feature data:", error));

    axios
      .get(uri_channel_feature)
      .then((response) => {
        const data = response.data[0]; // 데이터 가져오기
        const participationPercent = parseFloat(data["참여도"].replace('%', '')); // 참여도 값 (% 제거 후 숫자로 변환)
        const nonParticipationPercent = 100 - participationPercent; // 비구독자 비율

        const ctx = activationChartRef.current.getContext("2d"); // 캔버스 컨텍스트 가져오기

        const chartData = {
          labels: ["구독자 비율", "비구독자 비율"], // Doughnut 차트의 레이블
          datasets: [
            {
              data: [participationPercent, nonParticipationPercent], // 구독자 비율과 비구독자 비율 데이터
              backgroundColor: ["#4caf50", "#f44336"], // 각 데이터의 색상
              borderColor: ["#4caf50", "#f44336"], // 경계선 색상
              borderWidth: 1, // 경계선 두께
            },
          ],
        };

        // Doughnut 차트 생성
        new Chart(ctx, {
          type: "doughnut", // 차트 타입: Doughnut
          data: chartData,
          options: {
            responsive: true, // 반응형 옵션
            plugins: {
              legend: {
                display: true, // 범례 표시
              },
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    const label = tooltipItem.label;
                    const value = tooltipItem.raw;
                    return `${label}: ${value}%`; // 툴팁에 표시될 내용
                  },
                },
              },
            },
          },
        });
      })
      .catch((error) => console.error("Error fetching channel feature data:", error));
  }, [channelName]);


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
          <canvas ref={viewsChartRef} width="400" height="200"></canvas>
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
                    <div className="video-detail">
                      <span>노출 클릭률</span>
                      <span>{video["노출 클릭률"]}</span>
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
                    <div className="video-detail">
                      <span>노출 클릭률</span>
                      <span>{thumb["노출 클릭률"]}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p>로딩 중...</p> // ✅ 데이터 로딩 중 표시
            )}
          </div>
        </div>

        <div className="graph-card">
          <h3>채널 성장 추세</h3>
          <canvas ref={growthChartRef} width="400" height="200"></canvas>
        </div>

        <div className="graph-card">
          <h3>조회수 변화 그래프</h3>
          <canvas ref={viewsChangeChartRef} width="400" height="200"></canvas>
        </div>

        <div className="upload-cycle">
          <h3>영상 업로드 주기</h3>
          <canvas ref={uploadCycleChartRef} width="400" height="200"></canvas>
          <p>영상 업로드 주기가 불규칙적이에요. 규칙적인 업로드는 고정팬을 증가시켜 안정적인 조회수를 얻을 수 있어요.</p>
        </div>

        <div className="activation-metric">
          <h3>유사 채널 대비 활성도</h3>
          <canvas ref={activationChartRef} width="400" height="200"></canvas>
          <p>내 영상을 시청하는 사람 중 구독자의 비율이 높아요. 이는 팬덤이 어느 정도 형성되어 안정적인 채널 운영이 가능함을 의미합니다.</p>
        </div>
      </div>


    </div>
  );
};

export default Performance;
