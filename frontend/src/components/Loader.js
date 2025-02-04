import React from "react";
import ReactLoading from "react-loading";
import "./Loader.css"; // 스타일을 추가할 경우
import loadingGif from "./spinner.gif"; // GIF 파일 경로를 지정

const Loader = ({ type, color, message }) => {
  return (
    <div className="loader-container">
      <div className="loader-content">
        <h2>{message}</h2>
        <h3>창을 닫지 말아주세요.</h3>
        <img src={loadingGif} alt="Loading..." className="loader-gif" />
      </div>
    </div>
  );
};

export default Loader;
