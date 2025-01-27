import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Swot_Revenue.css";

const Revenue = () => {
  const navigate = useNavigate();

  // 데이터 객체 (임의 데이터, 실제 데이터가 아닌 더미 값)
  const data = {
    조회수: {
      내계정: 10000, // 내 계정의 조회수 수익
      평균값: 1000000000000, // DB에서 가져온 평균 조회수 수익
    },
    슈퍼챗: {
      내계정: 80000000, // 내 계정의 슈퍼챗 및 후원 수익
      평균값: 60000000, // DB에서 가져온 평균 슈퍼챗 및 후원 수익
    },
  };

  // 최대값 계산 (그래프의 비율 계산 기준으로 사용)
  const maxValue = Math.max(
    data.조회수.내계정,
    data.조회수.평균값,
    data.슈퍼챗.내계정,
    data.슈퍼챗.평균값
  );

  const MIN_WIDTH_PERCENTAGE = 5; // 그래프의 최소 너비 (비율로 5%)

  // 탭 상태 (현재 활성화된 탭을 저장)
  const [activeTab, setActiveTab] = useState("revenue");

  // 탭에 따라 콘텐츠를 렌더링하는 함수
  const renderContent = () => {
    if (activeTab === "revenue") {
      // '채널 수익성' 탭이 활성화된 경우
      return (
        <div className="revenue-content">
          <div className="grid-container">
            {/* 1: 조회수 수입 및 후원 수입 */}
            <section className="grid-item">
              <h2>조회수 수입 및 후원 수입</h2>

              {/* 조회수 그룹 */}
              <div className="chart-group">
                <h3>조회수</h3>

                {/* 조회수 (내 계정) */}
                <div className="bar-item">
                  <div
                    className="bar"
                    style={{
                      // 그래프 너비를 데이터 값에 비례하여 계산, 최소값 적용
                      width: `${Math.max(
                        (data.조회수.내계정 / maxValue) * 100,
                        MIN_WIDTH_PERCENTAGE
                      )}%`,
                    }}
                  ></div>
                  <p className="bar-label">{data.조회수.내계정.toLocaleString()}원</p>
                </div>

                {/* 조회수 (DB 평균값) */}
                <div className="bar-item">
                  <div
                    className="bar"
                    style={{
                      width: `${Math.max(
                        (data.조회수.평균값 / maxValue) * 100,
                        MIN_WIDTH_PERCENTAGE
                      )}%`,
                    }}
                  ></div>
                  <p className="bar-label">{data.조회수.평균값.toLocaleString()}원</p>
                </div>
              </div>

              {/* 슈퍼챗 및 후원 그룹 */}
              <div className="chart-group">
                <h3>슈퍼챗 및 후원</h3>

                {/* 슈퍼챗 및 후원 (내 계정) */}
                <div className="bar-item">
                  <div
                    className="bar"
                    style={{
                      width: `${Math.max(
                        (data.슈퍼챗.내계정 / maxValue) * 100,
                        MIN_WIDTH_PERCENTAGE
                      )}%`,
                    }}
                  ></div>
                  <p className="bar-label">{data.슈퍼챗.내계정.toLocaleString()}원</p>
                </div>

                {/* 슈퍼챗 및 후원 (DB 평균값) */}
                <div className="bar-item">
                  <div
                    className="bar"
                    style={{
                      width: `${Math.max(
                        (data.슈퍼챗.평균값 / maxValue) * 100,
                        MIN_WIDTH_PERCENTAGE
                      )}%`,
                    }}
                  ></div>
                  <p className="bar-label">{data.슈퍼챗.평균값.toLocaleString()}원</p>
                </div>
              </div>
            </section>

            {/* 2: 가장 성적이 좋은/안좋은 광고영상 */}
            <section className="grid-item">
              <h2>가장 성적이 좋은/안좋은 광고영상</h2>
              <div className="ad-row">
                {/* 가장 성적이 좋은 광고영상 */}
                <div className="ad-card">
                  <h3>둘이 실제로 만난 썰 (더미)</h3>
                  <p>업로드 날짜: 2025-01-17</p>
                  <ul>
                    <li>조회수: 120,000회</li>
                    <li>좋아요: 5,000개</li>
                    <li>댓글: 300개</li>
                    <li>클릭률: 4.3%</li>
                  </ul>
                </div>
                {/* 가장 성적이 좋지 않은 광고영상 */}
                <div className="ad-card">
                  <h3>실사 미쳤다 (더미)</h3>
                  <p>업로드 날짜: 2025-01-11</p>
                  <ul>
                    <li>조회수: 30,000회</li>
                    <li>좋아요: 1,000개</li>
                    <li>댓글: 50개</li>
                    <li>클릭률: 1.2%</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* 3: 광고 영상과 일반 영상의 성과 비교 */}
            <section className="grid-item">
              <h2>광고 영상과 일반 영상의 성과 비교</h2>
              <p>광고 영상과 일반 영상의 조회수, 좋아요, 댓글 수를 비교합니다. (더미 데이터)</p>
            </section>

            {/* 4: Hyper CLOVA X 분석 결과 */}
            <section className="grid-item">
              <h2>Hyper CLOVA X 분석 결과</h2>
              <p>Hyper CLOVA X의 세 가지 지표에 대한 분석 결과를 보여줍니다. (더미 데이터)</p>
            </section>
          </div>
        </div>
      );
    }
    return null; // 탭이 활성화되지 않은 경우 아무것도 렌더링하지 않음
  };

  return (
    <div className="revenue-container">
      {/* 탭 버튼 */}
      <div className="tabs">
        <button
          className={activeTab === "performance" ? "active" : ""}
          onClick={() => {
            setActiveTab("performance");
            navigate("/main/Swot/Performance");
          }}
        >
          채널 성과
        </button>
        <button
          className={activeTab === "engagement" ? "active" : ""}
          onClick={() => setActiveTab("engagement")}
        >
          시청자 참여도
        </button>
        <button
          className={activeTab === "revenue" ? "active" : ""}
          onClick={() => setActiveTab("revenue")}
        >
          채널 수익성
        </button>
      </div>

      {/* 탭 내용 */}
      <div className="tab-content">{renderContent()}</div>
    </div>
  );
};

export default Revenue;
