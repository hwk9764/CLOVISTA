import React, { useState } from 'react';
import './Signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSignup = (e) => {
    e.preventDefault();

    // 비밀번호 확인 로직
    if (formData.password !== formData.confirmPassword) {
      alert('비밀번호가 일치하지 않습니다.');
      return;
    }

    // 회원 정보 로컬 스토리지에 저장
    localStorage.setItem('user', JSON.stringify({
      name: formData.name,
      email: formData.email,
      password: formData.password,
    }));

    alert('회원가입이 완료되었습니다.');
    window.location.href = '/';
  };

  return (
    <div className="signup-container">
      <h2>회원가입</h2>
      <form className="signup-form" onSubmit={handleSignup}>
        <input
          type="text"
          name="name"
          placeholder="이름"
          className="input-field"
          value={formData.name}
          onChange={handleChange}
          required
        />
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
        <input
          type="password"
          name="confirmPassword"
          placeholder="비밀번호 확인"
          className="input-field"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        <button type="submit" className="signup-button">가입하기</button>
      </form>
      <a href="/" className="back-to-home">로그인 페이지로 돌아가기</a>
    </div>
  );
};

export default Signup;
