import os
import time
import json
import requests
from fastapi import HTTPException, APIRouter, UploadFile, File
from prs_cns.prompt import PROMPT_sensitive

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
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

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


# CompletionExecutor 객체 생성 및 실행
completion_executor = CompletionExecutor(
    host="https://clovastudio.stream.ntruss.com",
    api_key="Bearer nv-f5786fde571f424786ed0823986ca992h3P1",
    request_id="aca3cc2b98354bad93bbf15f4b63f616",
)


@sensitive_router.get("/result/{user_id}")
async def result(user_id: str):
    # 파일 확인
    user_id = "test"
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


@sensitive_router.post("/analysis/")
async def analysis(user_id: str, file: UploadFile = File(...)):
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
    all_text_add = f"제목: {title}\n스크립트: " + all_text
    print(all_text_add)

    formatted_prompt = [
        PROMPT_sensitive[0],
        {"role": "user", "content": PROMPT_sensitive[1]["content"].format(all_text_add)},
    ]
    request_data = {
        "messages": formatted_prompt,
        "topP": 0.7,
        "topK": 0,
        "maxTokens": 512,
        "temperature": 0.2,
        "repeatPenalty": 1.2,
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

    selected_text = pred.split("민감한 문장 추출:")[1].split("발생 가능성:")[0].strip()
    prob = pred.split("발생 가능성:")[1].split("심각성:")[0].strip()
    prob_score, prob_text = get_score_text(prob)
    danger = pred.split("심각성:")[1].split("영향 범위:")[0].strip()
    danger_score, danger_text = get_score_text(danger)
    scope = pred.split("영향 범위:")[-1].strip()
    scope_score, scope_text = get_score_text(scope)

    # 결과 저장
    output_json = {
        "selected_text": selected_text,
        "prob_score": prob_score,
        "prob_text": prob_text,
        "danger_score": danger_score,
        "danger_text": danger_text,
        "scope_score": scope_score,
        "scope_text": scope_text,
    }
    with open(upload_dir + "/" + title + ".json", "w") as json_file:
        json.dump(output_json, json_file, ensure_ascii=False, indent=4)

    return output_json
