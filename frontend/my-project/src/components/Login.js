import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import './Login.css';

const Login = ({ isPopup, onClose }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = () => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
  
    if (!storedUser || storedUser.email !== formData.email || storedUser.password !== formData.password) {
      setErrorMessage('잘못된 ID 혹은 비밀번호입니다.');
      return;
    }
  
    alert('로그인이 되었습니다!');
  
    if (storedUser.newUser) {
      alert('신규 이용자시군요?');
      navigate('/survey');  // 설문조사 페이지로 이동
    } else {
      navigate('/');  // 메인 페이지로 이동
    }
  
    onClose();
  };

  return (
    <div className={isPopup ? "popup-overlay" : "login-container"}>
      <div className={isPopup ? "popup-content" : "login-content"}>
        <h2 className="popup-title">로그인</h2>

        {errorMessage && <p className="error-message">{errorMessage}</p>}

        <form className="login-form" onSubmit={handleLogin}>
          <input
            type="email"
            name="email"
            placeholder="이메일"
            className="input-field"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="비밀번호"
            className="input-field"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit" className="login-button">
            로그인
          </button>
        </form>

        <div className="signup-section">
          아직 회원이 아니신가요? 
          <a onClick={() => navigate('/signup')} className="signup-link"> 회원가입하기</a>
        </div>

        <div className="social-login">
          <GoogleLogin
            onSuccess={(response) => {
              console.log('구글 로그인 성공:', response);
              alert('구글 로그인 성공!');
              if (isPopup && onClose) onClose();
            }}
            onError={(error) => {
              console.error('구글 로그인 실패:', error);
              setErrorMessage('구글 로그인에 실패했습니다.');
            }}
          />
        </div>

        {isPopup && <button className="close-button" onClick={onClose}>닫기</button>}
      </div>
    </div>
  );
};

export default Login;
