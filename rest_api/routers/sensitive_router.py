import time
import json
import requests
from fastapi import APIRouter
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


@sensitive_router.post("/result/{files}")
async def result(files: str):
    # mp.3 등 파일 받아서 TTS 진행

    # 우선 데모 파일에서 텍스트 추출
    ex1_text = ""
    with open("ex1.json", "r", encoding="utf-8") as file:
        ex1 = json.load(file)
        for x in ex1["segments"]:
            ex1_text += x.get("text") + " "

    # 전처리
    ex1_text_add = "제목: 대본 하나 없이 즉흥 애드립으로 웃기기\n스크립트: " + ex1_text

    print("#### 결과 출력 중")
    # # 결과 출력
    # formatted_prompt = [
    #     PROMPT_sensitive[0],
    #     {"role": "user", "content": PROMPT_sensitive[1]["content"].format(ex1_text_add)},
    # ]
    # request_data = {
    #     "messages": formatted_prompt,
    #     "topP": 0.7,
    #     "topK": 0,
    #     "maxTokens": 512,
    #     "temperature": 0.2,
    #     "repeatPenalty": 12,
    #     "stopBefore": [],
    #     "includeAiFilters": False,
    #     "seed": 104,
    # }
    # pred = completion_executor.execute_retry(request_data)
    pred = """민감한 문장 추출:
    1. "눈을 씨발 앞에서 사람이 말하는데" (탐지된 키워드/패턴: 욕설)
    2. "소개팅 딱 한번 해봤거든요. 시발 그거 트라우마 생겨서 진짜 안 한단 말이에요." (탐지된 키워드/패턴: 욕설, 트라우마)

    발생 가능성:
    - 점수: 높음 (7점)
    - 이유: 욕설과 트라우마를 언급하는 표현이 포함되어 있으며, 이러한 표현은 논란을 일으킬 가능성이 높습니다.
    - 개선 방안: 코미디 장르에서는 풍자적이고 과장된 표현이 용인되지만, 욕설과 트라우마를 언급하는 표현은 민감한 주제로 간주될 수 있으므로 주의가 필요합니다.

    심각성:
    - 점수: 중간 (3점)
    - 이유: 욕설과 트라우마를 언급하는 표현이 포함되어 있지만, 심각한 사회적, 경제적, 법적 영향을 미칠 가능성은 상대적으로 낮습니다.
    - 개선 방안: 심각한 영향을 미칠 가능성은 낮지만, 표현에 주의를 기울이고, 시청자들에게 불쾌감을 줄 수 있는 표현을 자제하는 것이 좋습니다.

    영향 범위:
    - 점수: 중간 (3점)
    - 이유: 지역적 이슈를 다루는 스텐드업 코미디로, 다양한 대상을 다루지는 않지만, 일부 시청자들에게 영향을 미칠 수 있습니다.
    - 개선 방안: 지역적 이슈를 다루더라도, 다양한 대상을 고려하여 표현을 선택하고, 시청자들의 다양한 관점을 존중하는 것이 좋습니다.
    """

    return pred
