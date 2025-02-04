import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import './Main.css';

const MainPage = () => {
  const [hasYouTubeChannel, setHasYouTubeChannel] = useState(null);

  useEffect(() => {
    const userInfo = JSON.parse(localStorage.getItem('user')) || {};
    setHasYouTubeChannel(userInfo.surveyResponses?.hasChannel === 'yes');
  }, []);

  return (
    <div className="main-container">
      <h1>Hyper CLOVA X를 통한 여러 인사이트를 경험해보세요!</h1>
      <p>Choose your Service</p>
      <div className="services">
        <ServiceCard
          title="맞춤형 채널 정책성 진단받아보기"
          description="유튜브 채널 운영을 위한 정책적 방향을 진단받아보세요."
        />
        {hasYouTubeChannel && (
          <ServiceCard
            title="내 유튜브 채널 SWOT 분석 받기"
            description="채널의 강점, 약점, 기회, 위협 요인을 분석해보세요."
            link='/main/Swot'
          />
        )}
        <ServiceCard
          title="영상 업로드 전 민감도 분석하기"
          description="영상이 업로드되기 전 민감도를 확인해보세요."
          link='/main/sense'
        />
      </div>
    </div>
  );
};

const ServiceCard = ({ title, description, link }) => {
  const navigate=useNavigate();

  const handleClick = () => {
    if (link) {
      navigate(link); // link가 있으면 해당 경로로 이동
    }
  };

  return (
  <div className="service-card" onClick={handleClick} style={{cursor:'pointer'}}>
    <h3>{title}</h3>
    <p>{description}</p>
  </div>
  );
};

export default MainPage;