import React, { useState } from 'react';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    const storedUser = JSON.parse(localStorage.getItem('user'));

    if (!storedUser || storedUser.email !== formData.email || storedUser.password !== formData.password) {
      setErrorMessage('잘못된 ID 혹은 비밀번호입니다.');
      return;
    }

    alert('로그인이 되었습니다!');
    window.location.href = '/';  // 메인 페이지로 이동
  };

  return (
    <div className="login-container">
      <h2>로그인</h2>
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
        <button type="button" className="login-button" onClick={() => console.log('로그인 버튼 클릭됨')}>
            로그인
        </button>
      </form>
    </div>
  );
};

export default Login;
