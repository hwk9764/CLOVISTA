import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Chart from "chart.js/auto";
import "./Swot_Revenue.css";
import axios from "axios";

const SwotRevenue = () => {
  const navigate = useNavigate();
  const chartRefViews = useRef(null); // 조회수 그래프
  const chartRefDonations = useRef(null); // 후원 수입 그래프
  const channelName = "너덜트"; // 채널 이름
  const [bestAd, setBestAd] = useState(null); // 가장 성적이 좋은 광고 영상 데이터 상태
  const [worstAd, setWorstAd] = useState(null); // 가장 성적이 안 좋은 광고 영상 데이터 상태
  const [comparisonData, setComparisonData] = useState(null); // 광고 영상 vs 일반 영상 성과 비교 데이터 상태
  const [analysisResult, setAnalysisResult] = useState(""); // 수익성 분석 결과


  useEffect(() => {
    const uriViewsDonations = `http://10.28.224.177:30635/dashboard/profitability/views-and-donations/${channelName}`;
    const uriAdPerformance = `http://10.28.224.177:30635/dashboard/profitability/ad-performance/${channelName}`;
    const uriAdVsNormal = `http://10.28.224.177:30635/dashboard/profitability/ad-vs-normal/${channelName}`;
    const uriProfitabilityAnalysis = `http://10.28.224.177:30635/chatbot/profitability/clova-analysis/${channelName}`;

    // 조회수 및 후원 데이터 가져오기
    axios
      .get(uriViewsDonations)
      .then((response) => {
        const apiData = response.data[0];
        const userAverage = apiData.조회수_유저[1];
        const averageAverage = apiData.조회수_평균[1];

        const donationUser =
          typeof apiData.후원_유저 === "number" ? apiData.후원_유저 : 0;
        const donationAverage =
          typeof apiData.후원_평균 === "number" ? apiData.후원_평균 : 0;

        const ctxViews = chartRefViews.current.getContext("2d");
        const viewsData = {
          labels: ["내 계정", "평균값"],
          datasets: [
            {
              label: "조회수 수입",
              data: [userAverage, averageAverage],
              backgroundColor: ["#EDF9DE", "#FBD8A8"],
              barThickness: 40,
            },
          ],
        };
        new Chart(ctxViews, {
          type: "bar",
          data: viewsData,
          options: {
            indexAxis: "x",
            responsive: true,
            plugins: { legend: { display: false } },
          },
        });

        const ctxDonations = chartRefDonations.current.getContext("2d");
        const donationsData = {
          labels: ["내 계정", "평균값"],
          datasets: [
            {
              label: "후원 수입",
              data: [donationUser, donationAverage],
              backgroundColor: ["#EDF9DE", "#FBD8A8"],
              barThickness: 40,
            },
          ],
        };
        new Chart(ctxDonations, {
          type: "bar",
          data: donationsData,
          options: {
            indexAxis: "x",
            responsive: true,
            plugins: { legend: { display: false } },
          },
        });
      })
      .catch((error) => console.error("Error fetching views and donations data:", error));

    // 광고 영상 데이터 가져오기
    axios
      .get(uriAdPerformance)
      .then((response) => {
        setBestAd(response.data["가장 성적이 좋은 광고 영상"]);
        setWorstAd(response.data["가장 성적이 안좋은 광고 영상"]);
      })
      .catch((error) => console.error("Error fetching ad performance data:", error));

    // 광고 영상 vs 일반 영상 데이터 가져오기
    axios
      .get(uriAdVsNormal)
      .then((response) => {
        setComparisonData(response.data[0]);
      })
      .catch((error) => console.error("Error fetching ad vs normal comparison data:", error));

    // 채널 수익성 분석 결과 가져오기
    axios
      .post(uriProfitabilityAnalysis, {})
      .then((response) => {
        setAnalysisResult(response.data); // 분석 결과 상태에 저장
      })
      .catch((error) => console.error("Error fetching profitability analysis:", error));
  }, [channelName]);


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

      <div className="ads-wrapper">
        {/* 가장 성적이 좋은 광고영상 */}
        <div className="ad-section">
          <h4>가장 성적이 좋은 광고영상</h4>
          {bestAd ? (
            <>
              <img src={bestAd.썸네일} alt="Best Ad" className="ad-thumbnail" />
              <div className="ad-content">
                <div className="ad-info">
                  <p className="ad-title">{bestAd.제목}</p>
                  <div className="ad-detail">
                    <span>업로드 날짜</span>
                    <span>{bestAd["업로드 날짜"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>조회수</span>
                    <span>{bestAd.조회수}</span>
                  </div>
                  <div className="ad-detail">
                    <span>평균 조회율</span>
                    <span>{bestAd["평균 조회율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>댓글 참여율</span>
                    <span>{bestAd["댓글 참여율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>좋아요 참여율</span>
                    <span>{bestAd["좋아요 참여율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>노출 클릭률</span>
                    <span>{bestAd["노출 클릭률"]}</span>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* 가장 성적이 안 좋은 광고영상 */}
        <div className="ad-section">
          <h4>가장 성적이 안 좋은 광고영상</h4>
          {worstAd ? (
            <>
              <img src={worstAd.썸네일} alt="Worst Ad" className="ad-thumbnail" />
              <div className="ad-content">
                <div className="ad-info">
                  <p className="ad-title">{worstAd.제목}</p>
                  <div className="ad-detail">
                    <span>업로드 날짜</span>
                    <span>{worstAd["업로드 날짜"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>조회수</span>
                    <span>{worstAd.조회수}</span>
                  </div>
                  <div className="ad-detail">
                    <span>평균 조회율</span>
                    <span>{worstAd["평균 조회율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>댓글 참여율</span>
                    <span>{worstAd["댓글 참여율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>좋아요 참여율</span>
                    <span>{worstAd["좋아요 참여율"]}</span>
                  </div>
                  <div className="ad-detail">
                    <span>노출 클릭률</span>
                    <span>{worstAd["노출 클릭률"]}</span>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>


        {/* 광고영상과 일반영상의 성과 비교 */}
        <div className="section">
          <h3>광고영상과 일반영상의 성과 비교</h3>
          {comparisonData ? (
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
                {Object.entries(comparisonData).map(([key, value]) => (
                  <tr key={key}>
                    <td>{key}</td>
                    <td>{value["일반 영상"]}</td>
                    <td>{value["광고 영상"]}</td>
                    <td>{value["비교"]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* 채널의 수익성 분석 결과 */}
        <div className="section">
          <h3>채널의 수익성에 대한 분석결과</h3>
          {analysisResult ? (
            <div className="analysis-box">{analysisResult}</div>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SwotRevenue;
