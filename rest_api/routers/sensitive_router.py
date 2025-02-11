import os
import time
import json
import requests
from fastapi import HTTPException, APIRouter, UploadFile, File, Form
from prompts.sensitivity_prompt import PROMPT_sensitive
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import ast

sensitive_router = APIRouter()

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id
        self._max_retries = 5

    def execute(self, completion_request):
        headers = {
            "Authorization": self._api_key,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
        }
        # POST 요청을 보냄 (스트리밍 대신 일반 요청)
        response = requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003", headers=headers, json=completion_request
        )

        # 응답 상태 확인
        if response.status_code == 200:
            response_data = response.json()
            return response_data["result"]["message"]["content"]
        else:
            # 에러 처리
            raise HTTPException(status_code=response.status_code, detail=response.text)

    def execute_retry(self, completion_request):
        headers = {
            "Authorization": self._api_key,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
        }

        retries = 0  # 현재 재시도 횟수
        while retries < self._max_retries:
            # POST 요청 보내기
            response = requests.post(
                self._host + "/testapp/v1/chat-completions/HCX-003", headers=headers, json=completion_request
            )

            # 응답 상태 확인
            if response.status_code == 200:
                response_data = response.json()
                return response_data["result"]["message"]["content"]
            elif response.status_code == 429:  # Too Many Requests
                print(f"Rate limit exceeded. Retrying after {1} seconds...")
                time.sleep(10)
                print(response.json())
                retries += 1
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)


# CompletionExecutor 객체 생성 및 실행
completion_executor = CompletionExecutor(
    host="https://clovastudio.stream.ntruss.com",
    api_key="Bearer nv-f5786fde571f424786ed0823986ca992h3P1",
    request_id="aca3cc2b98354bad93bbf15f4b63f616",
)


@sensitive_router.get("/result/{user_id}")
async def result(user_id: str):
    # 파일 확인
    upload_dir = f"./uploads/{user_id}"
    files = os.listdir(upload_dir)
    title = [x.split(".")[0] for x in files]
    title = set(title)

    # 분석 완료되었는지 확인
    result = []
    for t in title:
        output = {}
        t_ = t + ".json"
        if t_ in files:
            output["status"] = 1
            output["title"] = t
            with open(upload_dir + "/" + t_, "r", encoding="utf-8") as file:
                data = json.load(file)
            output.update(data)
            print(output)
        else:
            output["status"] = 0
            output["title"] = t
        result.append(output)

    return result


# CLOVA Speech API 요청
def clova_speech_stt(file_path):
    headers = {"X-CLOVASPEECH-API-KEY": "2f5cb96d73cf49459e862d2cc5be6407"}
    files = {
        "media": open(file_path, "rb"),
        "params": (None, json.dumps({"language": "ko-KR", "completion": "sync"}).encode("UTF-8"), "application/json"),
    }
    response = requests.post(
        "https://clovaspeech-gw.ncloud.com/external/v1/10094/9409a0f5da32cf23f7c4ecb52ef04a38ea2e6612670a3a4207613b2523ecf473/recognizer/upload",
        headers=headers,
        files=files,
    )
    return response.json()

def text_add(prompt, text, genre):
    text_add = f"채널의 장르: {genre}\n스크립트: " + text
    formatted_prompt = [prompt[0], {"role": "user", "content": prompt[1]["content"].format(text_add)}]
    return formatted_prompt

@sensitive_router.post("/analysis/")
async def analysis(user_id: str = Form(...), category: str = Form(...), file: UploadFile = File(...)):
    # 확장자 체크
    if file.filename.split(".")[-1] not in ["mp3", "mp4"]:
        raise HTTPException(status_code=400, detail="mp3, mp4 확장자로 올려주세요.")

    # 파일 이름 생성
    upload_dir = f"./uploads/{user_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    # 파일 저장
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print(f"{file_path} 저장 완료")

    # STT 실행
    result = clova_speech_stt(file_path)
    all_text = ""
    for x in result["segments"]:
        all_text += x.get("text") + " "
    print("STT 완료")

    # 민감도 분석 시작
    title = file.filename.split(".")[0]
    print(title)
    # all_text_add = f"제목: {title}\n스크립트: " + all_text
    # print(all_text_add)

    formatted_prompt = text_add(PROMPT_sensitive, all_text, category)
    request_data = {
        "messages": formatted_prompt,
        "topP": 0.8,
        "topK": 0,
        "maxTokens": 512,
        "temperature": 0.35,
        "repeatPenalty": 2.5,
        "stopBefore": [],
        "includeAiFilters": False,
        "seed": 104,
    }

    pred = completion_executor.execute_retry(request_data)
    print("민감도 분석 완료")
    print(pred)

    # 후처리
    def get_score_text(text):
        score = text.split("\n")[0].split(":")[-1].split("(")[0].strip()
        text = text.split("\n")[1:]
        text = "\n".join([x.strip() for x in text])
        return score, text

    selected_text = pred.split("민감한 문장: ")[1].split("발생 가능성: ")[0].strip()
    prob = pred.split("발생 가능성: ")[1].split("심각성: ")[0].strip()
    prob_score, prob_text = get_score_text(prob)
    danger = pred.split("심각성: ")[1].split("영향 범위: ")[0].strip()    #  변경
    danger_score, danger_text = get_score_text(danger)
    
    # controversy_type 가져오는 코드 수정 -> [논란 유형1, 논란 유형2, ..], '없음'인 경우는 빈 리스트로 반환
    controversy_type_line = pred.split("논란 유형: ")[1].split("발생 가능성:")[0].split('\n')
    controversy_type_line = [text.split('-')[1].strip().split('(')[0].strip() for text in controversy_type_line if text.strip() != '']
    controversy_types = None if len(controversy_type_line)==1 and controversy_type_line[0] == "없음" else controversy_type_line

    # --------------
    # 과거 논란 사례 제시
    try:
        df = pd.read_csv('/data/ephemeral/home/sh/level4-nlp-finalproject-hackathon-nlp-03-lv3/rest_api/routers/Controversy_Cases.csv')
        df['민감 발언'] = df['민감 발언'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else None)
        df['기사 링크'] = df['기사 링크'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else None)

    except Exception as e:
        print("Failed to load CSV:", e)
    
    result_df = df
    if controversy_types:
        for controversy_type in controversy_types:
            if'성적 발언' in controversy_type:
                result_df = result_df[result_df['논란 유형'] == '성 상품화']
            else:
                result_df = result_df[result_df['논란 유형'].str.contains(controversy_type, na=False)]
                
    if result_df.empty: # 뽑아낸 논란 유형이 csv에 없음
        lower = None    # 유사사례 나타내지 않음
    else:
        # 검색된 사례들의 대분류와 논란 유형 수집
        categories = set()
        types = set()
        for _, row in result_df.iterrows():
            if pd.notna(row['대분류']):
                categories.update(row['대분류'].split(', '))
            if pd.notna(row['논란 유형']):
                types.add(row['논란 유형'])

        ids = result_df['id'].tolist()
        controversy_intro = {
            "message": f"검색된 사례들은 다음 카테고리에 해당합니다: {', '.join(categories)}. 구체적인 논란 유형으로는 {', '.join(types)}이(가) 있습니다. 과거에 이 유형을 다룬 유튜브 크리에이터들 중에는 큰 논란이 일었던 적이 있으며, 아래에 관련한 사례가 예시로 주어집니다. 유사한 논란을 피하기 위해 관련 내용을 수정하거나 주의 깊게 다루는 것을 권장합니다.",
            "total_cases": len(result_df),
            "cases": ids
        }

        details, sensitive_speeches, controversy_articles = [], [], []
        for id in ids:
            try:
                controversy = df[df['id'] == id].iloc[0]
            except IndexError:
                raise HTTPException(status_code=404, detail="Record not found.")
            
            # 논란 카테고리 및 세부 유형, 영상 내용 설명
            detail = {
                "논란명": controversy['논란 내용'],
                "논란 카테고리": controversy['대분류'],
                "논란 세부유형": controversy['논란 유형'],
                "영상 내용": controversy['영상 내용']
            }
            details.append(detail)

            # 민감 발언과 발언의 부적절성, 혹은 컨텐츠의 부적절성
            sensitive_speech = {}
            if controversy['민감 발언']:
                sensitive_speech['문제 발언'] = [f"- 문제 발언 {index + 1}: {speech}" for index, speech in enumerate(controversy['민감 발언'])]
                sensitive_speech['발언의 부적절성'] = controversy['발언의 부적절성']
            else:
                sensitive_speech = {
                    "컨텐츠의 부적절성": controversy['컨텐츠의 부적절성']
                }
            sensitive_speeches.append(sensitive_speech)

            # 기사가 있으면 링크 나열
            if controversy['기사화 여부']:
                articles = {
                    f"기사 링크 {index + 1}": f"{item[0]} ({item[1]})"
                    for index, item in enumerate(controversy['기사 링크'])
                    if isinstance(item, list) and len(item) == 2
                }
                controversy_article = {
                    "message": "이 사건은 논란이 확산되자 기사화되었습니다. 다음은 관련 기사들의 목록입니다:",
                    "articles": articles
                }
            else:
                controversy_article = {"message": "이 사건에 대한 기사화된 내용은 없습니다."}
            controversy_articles.append(controversy_article)
            
        lower = {
            "controversy_types": controversy_types,
            "controversy_intro": controversy_intro,
            "controversy_details": details,
            "sensitive_speeches": sensitive_speeches,
            "controversy_articles": controversy_articles
        }
    # --------------
    
    # 결과 저장
    output_json = {
        "selected_text": selected_text,
        "prob_score": prob_score,
        "prob_text": prob_text,
        "danger_score": danger_score,
        "danger_text": danger_text,
        "lower": lower
    }
    with open(upload_dir + "/" + title + ".json", "w") as json_file:
        json.dump(output_json, json_file, ensure_ascii=False, indent=4)

    return output_json
