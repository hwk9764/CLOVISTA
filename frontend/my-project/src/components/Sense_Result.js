import React from 'react';
import { useParams } from 'react-router-dom';
import './Sense_Result.css';

const Sense_result = () => {
  const { id } = useParams(); // URL에서 전달받은 id
  const mockResults = {
    2: {
      title: '그렇게 구멍이 나나 봅니다 (쇼츠편집)',
      content: `
        해당 영상 대본에는 논란이 될 만한 내용이 없는 것 같습니다. 영상 속에서는 경제 관련 주제에 대해 이야기하고 있으며, 
        대화 형식으로 이루어져 있습니다. 또한 유튜버 수가급의 단순 입장가치 평가 주제, 부동산 등 다양한 경제 개념과 주제 
        분배에 대해 논리적으로 다루고 있습니다. 이러한 주제는 일반적으로 경제 관점에서 다루어지는 것으로, 특별한 논란의 여지가 없어 보입니다.
      `,
      notes: [
        '(01:05) 정보를 잘 찾는 방법을 알려 드리는 것처럼, 추가되는 정보보다 정보 찾는 방법이나 투자에 대한 시선을 전달하는 방식으로 요점을 잡는 것이 좋습니다.',
        '(04:19) 경제 주제와 사람들의 대화를 다루는 영상이기 때문에 새롭게 다룰 정보를 찾기 쉽지 않지만, 이번 사례에서는 큰 문제가 없어 보입니다.',
      ],
      score: 15,
    },
    // Add more mock data for other IDs
  };

  const result = mockResults[id];

  return (
    <div className="result-container">
      {result ? (
        <>
          <h2>{result.title}</h2>
          <div className="result-content">
            <p>{result.content}</p>
          </div>
          <div className="result-details">
            <ul>
              {result.notes.map((note, index) => (
                <li key={index}>{note}</li>
              ))}
            </ul>
          </div>
          <div className="result-score">
            <div className="gauge">
              <div className="gauge-fill" style={{ transform: `rotate(${result.score * 2.4}deg)` }}></div>
              <div className="gauge-cover">{result.score}점</div>
            </div>
          </div>
        </>
      ) : (
        <p>결과를 찾을 수 없습니다.</p>
      )}
    </div>
  );
};

export default Sense_result;
