import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Swot.css';

const SwotPage = () => {
    return (
        <div className="main-container">
            {/* 종합 분석 결과 */}
            <div className="summary-box">
                <h1>종합 분석 결과</h1>
                <p>
                    최근 영상 시청자 중 구독자의 비율이 70%로 높은 편이지만 100%가 아니기 때문에 잡수 구독자의 비율이 어느 정도 있을 것으로 예상됩니다. 하지만 타 유튜브 채널에 비해 낮은 편이므로 크게 문제가 되지 않을 것으로 보입니다.<br />
                    '한국지리 일타강사 문쌤'이라는 독특한 컨셉으로 인해 경쟁이 심한 코미디 카테고리 내에서도 비교적 우위에 있다고 볼 수 있습니다.
                </p>
            </div>

            {/* 서비스 카드 */}
            <div className="services">
                <ServiceCard
                    title="채널 성과 분석결과"
                    description="조회수, 구독자 증가율, 노출 클릭률 등 채널의 전반적인 성과를 분석 받아보세요."
                    link="/main/Swot/Performance"
                />

                <ServiceCard
                    title="시청자 참여도 분석결과"
                    description="좋아요, 댓글, 공유 등 시청자들의 참여도를 분석받아보세요."
                    link="/main/Swot/Engagement"
                />

                <ServiceCard
                    title="채널 수익성 분석결과"
                    description="광고 수익, 광고 영상의 마케팅 영향력 등 채널의 수익성에 대한 분석받아보세요."
                    link="/main/Swot/Revenue"
                />
            </div>
        </div>
    );
};

const ServiceCard = ({ title, description, link }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (link) {
            navigate(link);
        }
    };

    return (
        <div className="service-card" onClick={handleClick} style={{ cursor: 'pointer' }}>
            <h3>{title}</h3>
            <p>{description}</p>
            <button className="detail-button">자세한 분석결과 보러가기</button>
        </div>
    );
};

export default SwotPage;
