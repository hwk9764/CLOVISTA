import React, { useState } from 'react';
import LoginPopup from './components/LoginPopup';
import './App.css';

function App() {
  const [isPopupOpen, setPopupOpen] = useState(false);

  const handleOpenPopup = () => {
    setPopupOpen(true);
  };

  const handleClosePopup = () => {
    setPopupOpen(false);
  };

  return (
    <div className="container">
      <img src="/logo.png" alt="CLOVISTA Logo" className="logo" />
      <h1 className="title">CLOVISTA</h1>
      <h3 className="subtitle">Influencer Consultant Service with HyperCLOVA X</h3>
      <p className="description">
        CLOVISTA는 "CLOVA"와 라틴어로 "사이뷰"를 뜻하는 "VISTA"의 합성어로,
        HyperCLOVA X를 통해 유튜브 채널에 대한 깊이 있는 시선을 사용자에게 제공합니다.
      </p>
      <button className="chat-button" onClick={handleOpenPopup}>
        CLOVISTA와 대화하기
      </button>

      {isPopupOpen && <LoginPopup onClose={handleClosePopup} />}
    </div>
  );
}

export default App;
