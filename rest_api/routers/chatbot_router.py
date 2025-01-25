from fastapi import APIRouter, HTTPException, Depends, Request
import pandas as pd

chatbot_router = APIRouter()


def get_db_engine(request: Request):
    """
    FastAPI의 상태 객체에서 DB 엔진을 가져옵니다.
    """
    return request.app.state.db_engine


###################
## 채널 수익성 API ##
###################
@chatbot_router.post("/profitability/clova-analysis/{channel_name}")
async def analyze_profitability(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    CLOVA X를 이용해 채널의 수익성 분석 결과를 반환
    Return:
        - 논의 필요
    """
    return "ㅎㅇ"


###################
## 시청자 관계 API ##
###################
@chatbot_router.post("/audience/clova-analysis/{channel_name}")
async def analyze_audience_engagement(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    CLOVA X를 이용해 시청자의 참여도 분석 결과를 반환합니다.
    Return:
        - 논의 필요
    """

    return "ㅎㅇ"
