from fastapi import APIRouter, HTTPException, Depends, Request
import time
import requests
import json

HYPERCLOVA_API_URL = "https://clovastudio.stream.ntruss.com"
HYPERCLOVA_API_KEY = "Bearer nv-f5786fde571f424786ed0823986ca992h3P1"

recommendation_router = APIRouter()

def get_db_engine(request: Request):
    """
    FastAPI의 상태 객체에서 DB 엔진을 가져옵니다.
    """
    return request.app.state.db_engine

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
                
def call_hyperclova(answers):
    prompt = [{
        "role": "system",
        "content": """이제 막 유튜버의 꿈을 펼치려고 하는 사람이 있습니다. 이 초보 유튜버는 어떤 영상을 만들어야 할지, 채널의 방향을 어떻게 잡아야 할지 고민하고 있습니다. 초보 유튜버의 성공이 당신의 분석에 달렸습니다. 이 사람에게 맞는 채널 방향성과 정체성을 추천해주세요.
        아래 입력 정보를 바탕으로 이 사람에게 적합한 유튜브 채널 방향성과 정체성을 구체적으로 제안해주세요.
        ### 입력 정보:
        - 관심사 및 취미
        - 선호 콘텐츠 유형
        - 목표 시청자층
        - 영상 제작 가능 시간
        - 장비 및 예산
        - 콘텐츠 아이디어
        - 장기적인 목표
        
        ### 요청 사항:
        - 입력 정보를 종합적으로 분석하고, 각 항목에 초점을 맞추어 구체적인 제안을 작성하세요.
        - 각 정보가 서로 어떻게 연결되는지 고려하여 통합적인 방향성을 제시하세요.
        - 답변은 자연스러운 문장 서술 형태로 작성하되, 모든 입력 정보를 반영하세요.
        
        ### 참고:
        답변에는 다음 내용을 반드시 정확히 포함하세요:
        - 관심사와 선호 콘텐츠 유형, 목표 시청자층을 기반으로 한 채널 정체성 제안
        - 영상 제작 가능 시간을 고려한 업로드 일정 추천
        - 장비 및 예산 활용 방안 (제품 추천 포함)
        - 콘텐츠 아이디어의 구체적 활용법
        - 장기적인 목표 달성을 위한 조언
        """
    },
    {
        "role": "user", 
        "content": """관심사 및 취미 : {}
        선호 콘텐츠 유형 : {}
        목표 시청자층 : {}
        영상 제작 가능 시간 : {}
        장비 및 예산 : {}
        콘텐츠 아이디어 : {}
        장기적인 목표 : {}
        
        이 정보를 바탕으로 적합한 유튜브 채널 방향성과 정체성을 제안해주세요. 제공된 정보 중 부적절한 내용이 포함되어 있다면 분석을 거부하세요.
        """
    }]

    completion_executor = CompletionExecutor(
        host=HYPERCLOVA_API_URL,
        api_key=HYPERCLOVA_API_KEY,
        request_id='309fa53d16a64d7c9c2d8f67f74ac70d'
    )
    prompt = [prompt[0], {"role": "user", "content": prompt[1]['content'].format(answers["interest"], answers['contents'], answers['target'], answers['time'], answers['budget'], answers['creativity'], answers['goal'])}]
    request_data = {
                'messages': prompt,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 1024,
                'temperature': 0.35,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': False,
                'seed': 0
            }
    return completion_executor.execute(request_data)
    
@recommendation_router.get("/")
async def identity_recommendation(answers: json, db_engine=Depends(get_db_engine)):
    """
    채널 정체성 컨설팅, 콘텐츠 추천 HCX 답변 출력
    Parameters:
        7가지 질문에 대한 답변(관심사 및 취미, 선호 콘텐츠 유형, 목표 시청자층, 영상 제작 가능 시간, 장비 및 예산, 콘텐츠 아이디어, 장기적인 목표)
    Returns:
        Json
    """

    # 코드 테스트할 때는 try, except 빼는 것을 추천
    try:
        consulting = call_hyperclova(answers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return consulting