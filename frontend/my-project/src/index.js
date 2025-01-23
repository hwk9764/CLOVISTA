import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import Signup from './components/Signup';
import Login from './components/Login';  // 로그인 컴포넌트 추가
import Survey from './components/Survey';  // 설문조사 페이지 추가
import { GoogleOAuthProvider } from '@react-oauth/google';

ReactDOM.createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId="48244054796-8217g0gh724otkh1sl8r3fp7dfu0l5b8.apps.googleusercontent.com">
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/survey" element={<Survey />} />
      </Routes>
    </Router>
  </GoogleOAuthProvider>
);
