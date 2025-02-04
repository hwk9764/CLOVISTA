import React, { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import './Sense.css';

const Sense = () => {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0); // 업로드 진행 상태
  const navigate=useNavigate();


  const simulateFileUpload = () => {
    // 파일 업로드를 시뮬레이션 (예: API 호출 대체)
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setUploadProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 200);
  };

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setUploadProgress(0); // 초기화
      simulateFileUpload();
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const uploadedFile = e.dataTransfer.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setUploadProgress(0); // 초기화
      simulateFileUpload();
    }
  };

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const handleSensitivityCheck = () => {
    navigate('/main/senselist');
  };

  return (
    <div className="sense-container">
      <h2>영상 카테고리를 선택하고 영상을 업로드하세요!</h2>

      {/* Drag-and-Drop File Upload Section */}
      <div
        className={`file-upload-section ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p>눈금 아래로 영상을 드래그 앤 드롭하거나 버튼을 클릭하세요.</p>
        <input
          type="file"
          accept="video/mp4, video/mov, video/wmv, video/avi"
          onChange={handleFileUpload}
          id="file-input"
        />
        <label htmlFor="file-input" className="file-input-label">
          파일 선택
        </label>
        {file && <p className="file-name">선택된 파일: {file.name}</p>}
        {uploadProgress > 0 && (
          <div className="progress-bar-container">
            <div
              className="progress-bar"
              style={{ width: `${uploadProgress}%` }}
            ></div>
            <p>{uploadProgress}%</p>
          </div>
        )}
      </div>

      {/* Dropdown for Video Category */}
      <div className="dropdown-section">
        <label htmlFor="category">영상 카테고리를 골라주세요</label>
        <select
          id="category"
          value={selectedCategory}
          onChange={handleCategoryChange}
          className="dropdown"
        >
          <option value="">카테고리를 선택해주세요</option>
          <option value="entertainment">엔터테인먼트</option>
          <option value="education">교육</option>
          <option value="cooking">요리</option>
          <option value="sports">스포츠, 게임</option>
          <option value="music">음악</option>
        </select>
        {selectedCategory && <p className="category-selected">선택된 카테고리: {selectedCategory}</p>}
      </div>

      {/* 민감도 검사 버튼 */}
      {file && selectedCategory && (
        <button className="sensitivity-check-button" onClick={handleSensitivityCheck}>
          민감도 검사 받기
        </button>
      )}
    </div>
  );
};

export default Sense;
