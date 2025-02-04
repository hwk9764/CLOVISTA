import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './survey.css';

const Survey = () => {
  const navigate = useNavigate();
  const [hasChannel, setHasChannel] = useState(null);
  const [formData, setFormData] = useState({
    channelName: '',
    contentCategory: '',
    targetAge: '',
    targetGender: '',
  });

  const handleRadioChange = (e) => {
    setHasChannel(e.target.value);
    setFormData({
      channelName: '',
      contentCategory: '',
      targetAge: '',
      targetGender: '',
    });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // 사용자 정보 업데이트 (설문조사 응답 저장 및 신규 유저 상태 변경)
    const storedUser = JSON.parse(localStorage.getItem('user')) || {};
    storedUser.newUser = false;
    storedUser.surveyResponses = {
      hasChannel,
      ...formData,
    };
    console.log(localStorage)
    localStorage.setItem('user', JSON.stringify(storedUser));

    alert('설문조사가 완료되었습니다.');
    navigate('/main');
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', background: 'linear-gradient(to bottom, #e8f5c8, #d2edc4)', padding: '50px', borderRadius: '10px' }}>
      <h2>Survey</h2>
      <p>CLOVISTA의 맞춤형 분석을 위해 아래의 설문에 응답해주세요!</p>

      <div>
        <p>유튜브 채널이 있으신가요?</p>
        <label>
          <input type="radio" name="hasChannel" value="yes" onChange={handleRadioChange} /> 예
        </label>
        <label style={{ marginLeft: '20px' }}>
          <input type="radio" name="hasChannel" value="no" onChange={handleRadioChange} /> 아니오
        </label>
      </div>

      {hasChannel === 'yes' && (
        <>
          <div>
            <input
              type="text"
              name="channelName"
              placeholder="유튜브 채널 이름"
              value={formData.channelName}
              onChange={handleChange}
              style={{ display: 'block', margin: '10px auto', padding: '8px', width: '300px' }}
              required
            />
          </div>
          <div>
            <input
              type="text"
              name="contentCategory"
              placeholder="채널 주 컨텐츠"
              value={formData.contentCategory}
              onChange={handleChange}
              style={{ display: 'block', margin: '10px auto', padding: '8px', width: '300px' }}
              required
            />
          </div>
          <div>
            <p>주 타겟 구독자 연령</p>
            <select name="targetAge" onChange={handleChange} style={{ margin: '10px' }} required>
              <option value="">선택</option>
              <option value="10-20">10-20</option>
              <option value="20-30">20-30</option>
              <option value="30-40">30-40</option>
            </select>
          </div>
          <div>
            <p>주 타겟 구독자 성별</p>
            <select name="targetGender" onChange={handleChange} style={{ margin: '10px' }} required>
              <option value="">선택</option>
              <option value="남성">남성</option>
              <option value="여성">여성</option>
              <option value="그 외">그 외</option>
            </select>
          </div>
        </>
      )}

      {hasChannel === 'no' && (
        <>
          <div>
            <input
              type="text"
              name="contentCategory"
              placeholder="채널 주 컨텐츠"
              value={formData.contentCategory}
              onChange={handleChange}
              style={{ display: 'block', margin: '10px auto', padding: '8px', width: '300px' }}
              required
            />
          </div>
          <div>
            <p>주 타겟 구독자 연령</p>
            <select name="targetAge" onChange={handleChange} style={{ margin: '10px' }} required>
              <option value="">선택</option>
              <option value="10-20">10-20</option>
              <option value="20-30">20-30</option>
              <option value="30-40">30-40</option>
            </select>
          </div>
          <div>
            <p>주 타겟 구독자 성별</p>
            <select name="targetGender" onChange={handleChange} style={{ margin: '10px' }} required>
              <option value="">선택</option>
              <option value="남성">남성</option>
              <option value="여성">여성</option>
              <option value="그 외">그 외</option>
            </select>
          </div>
        </>
      )}

      {hasChannel && (
        <button onClick={handleSubmit} style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: 'black', color: 'white', border: 'none', borderRadius: '5px' }}>
          Submit
        </button>
      )}
    </div>
  );
};

export default Survey;
