import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import './LoginPopup.css';

const LoginPopup = ({ onClose }) => {
  const navigate = useNavigate();

  const handleGoogleSuccess = (response) => {
    console.log('구글 로그인 성공:', response);
  };

  const handleGoogleFailure = (error) => {
    console.error('구글 로그인 실패:', error);
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2 className="popup-title">로그인</h2>
        
        <input type="text" placeholder="아이디" className="input-field" />
        <input type="password" placeholder="비밀번호" className="input-field" />

        <button className="login-button">로그인</button>

        <div className="signup-section">
          아직 회원이 아니신가요? 
          <a onClick={() => navigate('/signup')} className="signup-link"> 회원가입하기</a>
        </div>

        <div className="social-login">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={handleGoogleFailure}
          />
        </div>

        <button className="close-button" onClick={onClose}>닫기</button>
      </div>
    </div>
  );
};

export default LoginPopup;
