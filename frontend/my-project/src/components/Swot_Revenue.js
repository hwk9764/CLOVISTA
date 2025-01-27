import React, { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Chart from "chart.js/auto";
import "./Swot_Revenue.css";

const SwotRevenue = () => {
  const navigate = useNavigate();
  const chartRefViews = useRef(null); // 조회수 그래프
  const chartRefDonations = useRef(null); // 후원 수입 그래프

  useEffect(() => {
    // 조회수 그래프
    const ctxViews = chartRefViews.current.getContext("2d");
    const viewsData = {
      labels: ["내 계정", "평균값"], // X축 레이블
      datasets: [
        {
          label: "조회수 수입",
          data: [2000000, 1000000], // 조회수 데이터
          backgroundColor: ["#EDF9DE", "#FBD8A8"], // 색상
          barThickness: 40,
        },
      ],
    };
    const viewsOptions = {
      indexAxis: "x", // 세로 막대 그래프
      responsive: true,
      plugins: {
        legend: {
          display: false, // 범례 표시
          position: "top",
        },
      },
    };
    new Chart(ctxViews, {
      type: "bar",
      data: viewsData,
      options: viewsOptions,
    });

    // 후원 수입 그래프
    const ctxDonations = chartRefDonations.current.getContext("2d");
    const donationsData = {
      labels: ["내 계정", "평균값"], // X축 레이블
      datasets: [
        {
          label: "후원 수입",
          data: [30000, 1000], // 후원 수입 데이터
          backgroundColor: ["#EDF9DE", "#FBD8A8"], // 색상
          barThickness: 40,
        },
      ],
    };
    const donationsOptions = {
      indexAxis: "x", // 세로 막대 그래프
      responsive: true,
      plugins: {
        legend: {
          display: false,
          position: "top",
        },
      },
    };
    new Chart(ctxDonations, {
      type: "bar",
      data: donationsData,
      options: donationsOptions,
    });
  }, []);

  return (
    <div className="revenue-container">
      {/* Toggle 버튼 영역 */}
      <div className="toggle-buttons">
        <button
          className="toggle-button"
          onClick={() => navigate("/main/Swot/Performance")}
        >
          채널 성과
        </button>
        <button
          className="toggle-button"
          onClick={() => navigate("/main/Swot/Engagement")}
        >
          시청자 참여도
        </button>
        <button
          className="toggle-button active"
          onClick={() => navigate("/main/Swot/Revenue")}
        >
          채널 수익성
        </button>
      </div>

      <div className="grid-container">
        {/* 조회수 및 후원 수입 섹션 */}
        <div className="section full-width">
          <h3>조회수 수입 및 후원 수입</h3>
          <div className="charts-wrapper">
            <div className="chart">
              <div>조회수</div>
              <canvas ref={chartRefViews} id="viewsChart" width="400" height="200"></canvas>
            </div>
            <div className="chart">
              <div>후원</div>
              <canvas ref={chartRefDonations} id="donationsChart" width="400" height="200"></canvas>
            </div>
          </div>
        </div>

        {/* 가장 성적이 좋은 광고영상과 가장 성적이 안 좋은 광고영상 */}
        <div className="section">
          <div className="ads-wrapper">
            {/* 가장 성적이 좋은 광고영상 */}
            <div className="ad-section">
              <h4>가장 성적이 좋은 광고영상</h4>
              <img src="/example_thumbnail.png" alt="Best Ad" className="ad-thumbnail" />
              <div className="ad-content">
              <div className="ad-info">
                  <p className="ad-title">용의 꼬리 vs 뱀의 머리 무엇으로 살 것인가?</p>
                  <div className="ad-detail">
                    <span>업로드 날짜</span>
                    <span>2025-01-17</span>
                  </div>
                  <div className="ad-detail">
                    <span>조회수</span>
                    <span>120만</span>
                  </div>
                  <div className="ad-detail">
                    <span>평균 조회율</span>
                    <span>17%</span>
                  </div>
                  <div className="ad-detail">
                    <span>댓글 참여율</span>
                    <span>0.31%</span>
                  </div>
                  <div className="ad-detail">
                    <span>좋아요 참여율</span>
                    <span>3.49%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* 가장 성적이 안 좋은 광고영상 */}
            <div className="ad-section">
              <h4>가장 성적이 안 좋은 광고영상</h4>
              <img src="/example_thumbnail_2.png" alt="Worst Ad" className="ad-thumbnail" />
              <div className="ad-content">
                <div className="ad-info">
                <p className="ad-title">실사 미쳤다</p>
                <div className="ad-detail">
                  <span>업로드 날짜</span>
                  <span>2025-01-11</span>
                </div>
                <div className="ad-detail">
                  <span>조회수</span>
                  <span>30만</span>
                </div>
                <div className="ad-detail">
                  <span>평균 조회율</span>
                  <span>4%</span>
                </div>
                <div className="ad-detail">
                  <span>댓글 참여율</span>
                  <span>0.11%</span>
                </div>
                <div className="ad-detail">
                  <span>좋아요 참여율</span>
                  <span>1.69%</span>
                </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 광고영상과 일반영상의 성과 비교 */}
        <div className="section">
          <h3>광고영상과 일반영상의 성과 비교</h3>
          <div className="video-summary">
            <div className="video-stat">
              <p><strong>광고 영상:</strong> 35개</p>
            </div>
            <div className="video-stat">
              <p><strong>누적 조회수:</strong> 1,200만</p>
            </div>
            <div className="video-stat">
              <p><strong>누적 좋아요:</strong> 33.7만</p>
            </div>
            <div className="video-stat">
              <p><strong>누적 댓글:</strong> 7천</p>
            </div>
          </div>
          <table className="comparison-table">
            <thead>
              <tr>
                <th>항목</th>
                <th>일반영상</th>
                <th>광고영상</th>
                <th>비교</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>영상수</td>
                <td>50</td>
                <td>20</td>
                <td>-</td>
              </tr>
              <tr>
                <td>업로드 주기</td>
                <td>주 2회</td>
                <td>주 1회</td>
                <td>-</td>
              </tr>
              <tr>
                <td>평균 조회수</td>
                <td>10만</td>
                <td>50만</td>
                <td>광고영상↑</td>
              </tr>
              <tr>
                <td>평균 좋아요 비율</td>
                <td>5%</td>
                <td>10%</td>
                <td>광고영상↑</td>
              </tr>
              <tr>
                <td>평균 댓글 비율</td>
                <td>2%</td>
                <td>4%</td>
                <td>광고영상↑</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* 채널의 수익성에 대한 분석결과 */}
        <div className="section">
          <h3>채널의 수익성에 대한 분석결과</h3>
          <p>이 섹션에 관련 내용을 추가하세요.</p>
        </div>
      </div>
    </div>
  );
};

export default SwotRevenue;
