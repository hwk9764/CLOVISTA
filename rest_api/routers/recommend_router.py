from fastapi import APIRouter, HTTPException, Depends, Request
import time
import requests
from typing import Dict, Any
from prompts.recommend_prompt import PROMPT_identity, PROMPT_content

HYPERCLOVA_API_URL = "https://clovastudio.stream.ntruss.com"
HYPERCLOVA_API_KEY = "Bearer nv-f5786fde571f424786ed0823986ca992h3P1"

recommendation_router = APIRouter()

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

        retries = 0  # 현재 재시도 횟수
        while retries < self._max_retries:
            # POST 요청 보내기
            response = requests.post(
                self._host + "/testapp/v1/chat-completions/HCX-003",
                headers=headers,
                json=completion_request
            )

            # 응답 상태 확인
            if response.status_code == 200:
                response_data = response.json()
                return response_data['result']["message"]["content"]
            elif response.status_code == 429:  # Too Many Requests
                print(f"Rate limit exceeded. Retrying after {1} seconds...")
                time.sleep(10)
                print(response.json())
                retries+=1

def call_hyperclova(answers, PROMPT):
    completion_executor = CompletionExecutor(
        host=HYPERCLOVA_API_URL,
        api_key=HYPERCLOVA_API_KEY,
        request_id='309fa53d16a64d7c9c2d8f67f74ac70d'
    )
    prompt = [PROMPT[0], {"role": "user", "content": PROMPT[1]['content'].format(answers["interest"], answers['contents'], answers['target'], answers['time'], answers['budget'], answers['creativity'], answers['goal'])}]
    request_data = {
                'messages': prompt,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 1024,
                'temperature': 0.35,
                'repeatPenalty': 2.5,
                'stopBefore': [],
                'includeAiFilters': False,
                'seed': 0
            }
    return completion_executor.execute(request_data)


def identity(answers):
    return call_hyperclova(answers, PROMPT_identity)

def contents(answers):
    return call_hyperclova(answers, PROMPT_content)

@recommendation_router.post("/")
async def recommendation(answers: Dict[str, Any]):
    """
    채널 정체성 컨설팅, 콘텐츠 추천 HCX 답변 출력
    Parameters:
        7가지 질문에 대한 답변(관심사 및 취미, 선호 콘텐츠 유형, 목표 시청자층, 영상 제작 가능 시간, 장비 및 예산, 콘텐츠 아이디어, 장기적인 목표)
    Returns:
        [{
            '정체성 추천':,
            ' 콘텐츠 추천':            
        }]
    """
    print('answrs : ', answers)
    try:
        recommended_identity = identity(answers)
        recommended_contents = contents(answers)
        result = {
            '정체성 추천': recommended_identity,
            '콘텐츠 추천': recommended_contents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return result