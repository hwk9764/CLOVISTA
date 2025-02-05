import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PopupGuide from "./PopupGuide";
import axios from 'axios';
import './Sense.css';

const Sense = () => {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [showPopup, setShowPopup] = useState(true); // popup trend
  const [isUploaded,setIsUploaded]=useState(false);

  const navigate = useNavigate();

  // localStorage에서 user 정보 가져오기
  const userData = JSON.parse(localStorage.getItem("user") || "{}");
  const userID = encodeURIComponent(userData.name || "unknown"); // name을 id로 사용

  // 파일 선택 이벤트 핸들러
  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile); // file 상태 업데이트
      setIsUploaded(true);
    }
  };

  // 파일이 설정되었을 때 업로드 시작
  useEffect(() => {
    if (file) {
      handleFileUploadComplete();
    }
  }, [file]);

  // 파일 업로드 후 서버로 전송
  const handleFileUploadComplete = async () => {
    if (!file) {
      console.error("🚨 파일이 없습니다.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file, file.name);

    try {
      const response = await axios.post(
        `http://10.28.224.177:30635/sensitive/analysis/?user_id=${userID}`,
        formData,
        {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      console.log("✅ 업로드 성공:", response.data);
      // alert("🎉 영상 업로드 성공!");
    } catch (error) {
      console.error("❌ 업로드 실패:", error);
      // alert("⚠️ 영상 업로드 실패. 다시 시도해주세요.");
    } finally {
    }
  };

  // Drag & Drop 이벤트 핸들링
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
    }
  };
  const closePopup = () => {
    setShowPopup(false);
  }
  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const handleSensitivityCheck = () => {
    navigate('/main/senselist');
  };

  return (
    <div className="sense-container">
      {/*pop up page*/}
      {/* {showPopup && (
        <PopupGuide
          onClose={closePopup}
        />
      )} */}
      <h2>영상 카테고리를 선택하고 영상을 업로드하세요!</h2>

      {/* Drag-and-Drop File Upload Section */}
      <div
        className={`file-upload-section ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isUploaded ? (
          <p className="upload-success">✅ {file.name} <br/> 업로드 완료!</p>
        ) : (
          <>
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
          </>
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
      <button className="sensitivity-check-button" onClick={handleSensitivityCheck}>
        민감도 검사 결과보기
      </button>
    </div>
  );
};

export default Sense;
