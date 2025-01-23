import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Survey = () => {
  const navigate = useNavigate();
  const [answer, setAnswer] = useState(null);

  const handleAnswer = (response) => {
    setAnswer(response);

    // 사용자 정보 업데이트 (설문조사 응답 저장 및 newUser 상태 변경)
    const storedUser = JSON.parse(localStorage.getItem('user'));
    if (storedUser) {
      storedUser.newUser = false;  // 신규 유저 상태 변경
      storedUser.surveyResponses = { youtubeChannel: response };  // 응답 저장

      localStorage.setItem('user', JSON.stringify(storedUser));
    }

    alert('설문조사가 완료되었습니다.');
    navigate('/');  // 메인 페이지로 이동
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>신규 이용자시군요?</h2>
      <p>본인의 유튜브 채널이 있으신가요?</p>
      <button onClick={() => handleAnswer('yes')} style={{ marginRight: '10px' }}>예</button>
      <button onClick={() => handleAnswer('no')}>아니오</button>
    </div>
  );
};

export default Survey;
