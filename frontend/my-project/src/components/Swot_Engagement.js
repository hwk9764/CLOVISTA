import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bar, Doughnut } from 'react-chartjs-2';
import axios from 'axios';
import GaugeChart from './GaugeChart.js'; // ✅ 기존 GaugeChart 유지
import './Swot_Engagement.css';

const SwotEngagement = () => {
  const navigate = useNavigate();

  // 상태 변수 (API 데이터 저장)
  const [liveComparison, setLiveComparison] = useState(null);
  const [averageLiveViewers, setAverageLiveViewers] = useState(null);
  const [audienceGender, setAudienceGender] = useState(null);
  const [audienceAge, setAudienceAge] = useState(null);
  const [recentKeywords, setRecentKeywords] = useState([]);
  const [videoTypeRatio, setVideoTypeRatio] = useState(null);
  const [uploadTime, setUploadTime] = useState(null);
  const [viewingTime, setViewingTime] = useState(null);
  const [channelEngagement, setChannelEngagement] = useState(null); // ✅ 추가

  // API 요청
  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseLiveComparison = await axios.get('/api/live_comparison');
        const responseAverageLiveViewers = await axios.get('/api/average_live_viewers');
        const responseAudience = await axios.get('/api/audience_data');
        const responseKeywords = await axios.get('/api/recent_keywords');
        const responseVideoTypeRatio = await axios.get('/api/video_type_ratio');
        const responseUploadViewingTime = await axios.get('/api/upload_viewing_time');
        const responseChannelEngagement = await axios.get('/api/channel_engagement'); // ✅ 추가

        setLiveComparison(responseLiveComparison.data);
        setAverageLiveViewers(responseAverageLiveViewers.data);
        setAudienceGender(responseAudience.data.gender);
        setAudienceAge(responseAudience.data.age);
        setRecentKeywords(responseKeywords.data);
        setVideoTypeRatio(responseVideoTypeRatio.data);
        setUploadTime(responseUploadViewingTime.data.upload_time);
        setViewingTime(responseUploadViewingTime.data.viewing_time);
        setChannelEngagement(responseChannelEngagement.data); // ✅ 추가
      } catch (error) {
        console.error('데이터 불러오기 오류:', error);
      }
    };

    fetchData();
  }, []);

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
        {/* ✅ 시청자의 채널 참여도 */}
        <div className="section">
          <h2 className="section-title">시청자의 채널 참여도</h2>
          <div className="gauge-container">
            {channelEngagement ? (
              <>
                <GaugeChart label="좋아요 비율" value={channelEngagement.likeRatio} color="#D9534F" />
                <GaugeChart label="댓글 비율" value={channelEngagement.commentRatio} color="#F0AD4E" />
                <GaugeChart label="공유 비율" value={channelEngagement.shareRatio} color="#5CB85C" />
              </>
            ) : (
              <p>데이터 없음</p>
            )}
          </div>
        </div>

        {/* 크리에이터의 소통 활동 */}
        <div className="section">
          <h2 className="section-title">크리에이터의 소통 활동</h2>
          <div className="chart-container">
            {liveComparison && (
              <div className="bar-chart">
                <h3>경쟁 채널과 비교한 최근 30일 라이브 수</h3>
                <Bar data={liveComparison} />
              </div>
            )}
            {averageLiveViewers && (
              <div className="gauge-chart">
                <h3>라이브 평균 시청자 수</h3>
                <Doughnut data={averageLiveViewers} />
              </div>
            )}
          </div>
        </div>

        {/* 시청자 타겟팅 전략 */}
        <div className="section">
          <h2 className="section-title">시청자 타겟팅 전략</h2>
          <div className="target-audience-container">
            {audienceGender && (
              <div className="doughnut-chart">
                <h3>타겟 시청자 특성 (성별)</h3>
                <Doughnut data={audienceGender} />
              </div>
            )}
            {audienceAge && (
              <div className="doughnut-chart">
                <h3>연령별 분포</h3>
                <Doughnut data={audienceAge} />
              </div>
            )}
          </div>

          {/* 최근 영상 키워드 */}
          <div className="keywords-container">
            <h3>최근 영상 키워드</h3>
            <div className="keyword-tags">
              {recentKeywords.length > 0
                ? recentKeywords.map((keyword, index) => (
                    <span key={index} className="keyword-tag">
                      {keyword}
                    </span>
                  ))
                : '데이터 없음'}
            </div>
          </div>
        </div>

        {/* 업로드 시간대 비교 */}
        <div className="section">
          <h2 className="section-title">업로드 시간대 비교</h2>
          <div className="upload-time-container">
            <div className="upload-time-text">
              <h3>영상 업로드 시간</h3>
              <p>{uploadTime || '데이터 없음'}</p>
              <h3>주요 시청 시간</h3>
              <p>{viewingTime || '데이터 없음'}</p>
            </div>

            {videoTypeRatio && (
              <div className="doughnut-chart">
                <h3>일반 / 광고 영상 비율</h3>
                <Doughnut data={videoTypeRatio} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SwotEngagement;
