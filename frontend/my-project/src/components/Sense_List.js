import React, { useState } from 'react';
import './Sense_List.css';

const SenseList = () => {
  // 가상 데이터 생성
  const mockData = Array.from({ length: 40 }, (_, i) => ({
    id: i + 1,
    title: `업로드된 영상 제목 ${i + 1}`,
    date: `2025.01.${String(24 - (i % 3)).padStart(2, '0')}`,
    format: i % 2 === 0 ? '.mp4' : '.avi',
    status: i % 3 === 0 ? '분석 중' : i % 3 === 1 ? '결과 보기' : '오류',
  }));

  const [currentPage, setCurrentPage] = useState(1); // 현재 페이지
  const itemsPerPage = 10; // 페이지당 항목 수
  const totalPages = Math.ceil(mockData.length / itemsPerPage);

  // 현재 페이지에 표시할 데이터
  const currentItems = mockData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // 페이지 변경 핸들러
  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="sense-list-container">
      <h2>민감도 검사 결과 목록</h2>
      <div className="search-container">
        <input type="text" placeholder="Search" className="search-input" />
        <select className="sort-select">
          <option value="newest">Sort by: Newest</option>
          <option value="oldest">Sort by: Oldest</option>
        </select>
      </div>
      <table className="sense-list-table">
        <thead>
          <tr>
            <th>업로드된 영상 제목</th>
            <th>검사 날짜</th>
            <th>파일 형식</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.map((item) => (
            <tr key={item.id}>
              <td>{item.title}</td>
              <td>{item.date}</td>
              <td>{item.format}</td>
              <td>
                <span
                  className={`status-label ${
                    item.status === '분석 중'
                      ? 'status-pending'
                      : item.status === '결과 보기'
                      ? 'status-completed'
                      : 'status-error'
                  }`}
                >
                  {item.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        {Array.from({ length: totalPages }, (_, i) => (
          <button
            key={i + 1}
            className={`page-button ${
              currentPage === i + 1 ? 'active' : ''
            }`}
            onClick={() => handlePageChange(i + 1)}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SenseList;
