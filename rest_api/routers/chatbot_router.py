from fastapi import APIRouter, HTTPException, Depends, Request
import requests
import pandas as pd
import json

chatbot_router = APIRouter()


class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            "Authorization": self._api_key,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }
        response_content = ""
        with requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003", headers=headers, json=completion_request, stream=True
        ) as r:
            for line in r.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    if data.startswith("data:"):
                        json_data = json.loads(data[5:])
                        if "message" in json_data and "content" in json_data["message"]:
                            response_content = json_data["message"]["content"]
        return response_content


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
    from prs_cns.prompt import PROMPT_revenue

    query = """
        SELECT
            COUNT(*) as total_videos,
            COUNT(*) FILTER (WHERE "hasPaidProductPlacement" = true) as sponsored_count
        FROM public."Video" v
        JOIN public."Channel" c ON v.channel_id = c.id
        WHERE c.name = %s
    """
    df = pd.read_sql(query, db_engine, params=(channel_name,))

    metrics = {"total_videos": df.iloc[0]["total_videos"], "sponsored_count": df.iloc[0]["sponsored_count"]}

    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="Bearer nv-f5786fde571f424786ed0823986ca992h3P1",
        request_id="309fa53d16a64d7c9c2d8f67f74ac70d",
    )

    formatted_prompt = [PROMPT_revenue[0], {"role": "user", "content": PROMPT_revenue[1]["content"].format(**metrics)}]

    request_data = {
        "messages": formatted_prompt,
        "topP": 0.8,
        "maxTokens": 2000,
        "temperature": 0.15,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeAiFilters": False,
        "seed": 0,
    }

    return completion_executor.execute(request_data)


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
    from prs_cns.prompt import PROMPT_relation

    query = """
        WITH channel_stats AS (
            SELECT 
                c.name,
                COUNT(*) FILTER (WHERE v."liveBroadcastContent" = 'true') as live_count,
                SUM(CAST(v."commentCount" AS INTEGER)) * 100.0 / NULLIF(SUM(CAST(v."videoViewCount" AS INTEGER)), 0) as comment_ratio,
                SUM(CAST(v."videoLikeCount" AS INTEGER)) * 100.0 / NULLIF(SUM(CAST(v."videoViewCount" AS INTEGER)), 0) as like_ratio,
                COUNT(*) FILTER (WHERE v."hasPaidProductPlacement" = true) * 100.0 / NULLIF(COUNT(*), 0) as sponsored_ratio
            FROM public."Channel" c
            JOIN public."Video" v ON c.id = v.channel_id
            GROUP BY c.name
        ),
        channel_ranks AS (
            SELECT 
                name,
                live_count,
                comment_ratio,
                like_ratio,
                sponsored_ratio,
                COUNT(*) OVER() as total_channels,
                RANK() OVER (ORDER BY live_count DESC) as live_rank,
                RANK() OVER (ORDER BY comment_ratio DESC) as comment_rank,
                RANK() OVER (ORDER BY like_ratio DESC) as like_rank
            FROM channel_stats
        )
        SELECT * FROM channel_ranks WHERE name = %s
    """
    df = pd.read_sql(query, db_engine, params=(channel_name,))

    if df.empty:
        raise HTTPException(status_code=404, detail="Channel not found")

    metrics = {
        "live_count": df.iloc[0]["live_count"],
        "live_total": df.iloc[0]["total_channels"],
        "live_rank": df.iloc[0]["live_rank"],
        "comment_ratio": df.iloc[0]["comment_ratio"],
        "comment_total": df.iloc[0]["total_channels"],
        "comment_rank": df.iloc[0]["comment_rank"],
        "like_ratio": df.iloc[0]["like_ratio"],
        "like_total": df.iloc[0]["total_channels"],
        "like_rank": df.iloc[0]["like_rank"],
        "sponsored_ratio": df.iloc[0]["sponsored_ratio"],
    }

    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="Bearer nv-f5786fde571f424786ed0823986ca992h3P1",
        request_id="309fa53d16a64d7c9c2d8f67f74ac70d",
    )

    formatted_prompt = [
        PROMPT_relation[0],
        {"role": "user", "content": PROMPT_relation[1]["content"].format(**metrics)},
    ]

    request_data = {
        "messages": formatted_prompt,
        "topP": 0.8,
        "maxTokens": 2000,
        "temperature": 0.15,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeAiFilters": False,
        "seed": 0,
    }

    return completion_executor.execute(request_data)


###################
## 채널 성과 API ##
###################
@chatbot_router.post("/performance/clova-analysis/{channel_name}")
async def analyze_performance_engagement(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    CLOVA X를 이용해 채널 성과 분석 결과를 반환합니다.
    Return:
        - 논의 필요
    """
    from prs_cns.prompt import PROMPT_performance

    query = """
        WITH video_stats AS (
            SELECT 
                c.name,
                COUNT(*) FILTER (WHERE CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '180 days') as uploads_6months,
                AVG(CAST(v."videoViewCount" AS FLOAT)) as avg_views
            FROM public."Channel" c
            JOIN public."Video" v ON c.id = v.channel_id
            GROUP BY c.name
        )
        SELECT 
            uploads_6months as monthly_uploads,
            avg_views
        FROM video_stats 
        WHERE name = %s
    """

    df = pd.read_sql(query, db_engine, params=(channel_name,))

    if df.empty:
        raise HTTPException(status_code=404, detail="Channel not found")

    metrics = {"monthly_uploads": df.iloc[0]["monthly_uploads"], "avg_views": df.iloc[0]["avg_views"]}

    completion_executor = CompletionExecutor(
        host="https://clovastudio.stream.ntruss.com",
        api_key="Bearer nv-f5786fde571f424786ed0823986ca992h3P1",
        request_id="309fa53d16a64d7c9c2d8f67f74ac70d",
    )

    formatted_prompt = [
        PROMPT_performance[0],
        {"role": "user", "content": PROMPT_performance[1]["content"].format(**metrics)},
    ]

    request_data = {
        "messages": formatted_prompt,
        "topP": 0.8,
        "maxTokens": 2000,
        "temperature": 0.15,
        "repeatPenalty": 5.0,
        "stopBefore": [],
        "includeAiFilters": False,
        "seed": 0,
    }

    return completion_executor.execute(request_data)
