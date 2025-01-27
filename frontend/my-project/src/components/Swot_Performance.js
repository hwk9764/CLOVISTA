import React from 'react';
import './Swot_Performance.css';

const Performance = () => {
  return (
    <div className="performance-container">
      <div className="grid-container">
        <div className="profile-section">
          <div className="profile-content">
            <img src="/path-to-profile-image" alt="Channel Profile" className="profile-image" />
            <div className="profile-info">
              <h2 className="channel-name">빠더너스 BDNS</h2>
              <p className="channel-stats">구독자 178만명, 동영상 1.2천개</p>
            </div>
          </div>
        </div>

        <div className="graph-section">
          <h3>채널 평균 조회수 및 경쟁 채널 평균 조회수</h3>
          <div className="bar-chart">
            <div className="bar my-channel">
              <span>내 채널 평균 조회수</span>
              <div className="bar-fill" style={{ width: '80%' }}></div>
              <span className="bar-value">100,921,304회</span>
            </div>
            <div className="bar competitor-channel">
              <span>경쟁 채널 평균 조회수</span>
              <div className="bar-fill" style={{ width: '50%' }}></div>
              <span className="bar-value">50,921,214회</span>
            </div>
          </div>
        </div>

        <div className="popular-videos">
          <h3>많은 사랑을 받은 영상</h3>
          <div className="video-list">
            {[1,2,3].map(index => (
              <div className="video-card" key={index}>
                <img src="/path-to-thumbnail" alt="Thumbnail" className="thumbnail" />
                <p className="video-title">영상 제목 {index}</p>
                <p className="video-stats">조회수: 14k</p>
                <p className="video-stats">평균 조회율: 15%</p>
                <p className="video-stats">댓글 참여율: 1.3%</p>
                <p className="video-stats">좋아요 참여율: 2.4%</p>
              </div>
            ))}
          </div>
        </div>

        <div className="popular-thumbnails">
          <h3>많은 사랑을 받은 썸네일</h3>
          <div className="video-list">
            {[1,2,3].map(index => (
              <div className="video-card" key={index}>
                <img src="/path-to-thumbnail" alt="Thumbnail" className="thumbnail" />
                <p className="video-title">썸네일 {index}</p>
                <p className="video-stats">조회수: 14k</p>
                <p className="video-stats">평균 조회율: 15%</p>
                <p className="video-stats">댓글 참여율: 1.3%</p>
                <p className="video-stats">좋아요 참여율: 2.4%</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Performance;
