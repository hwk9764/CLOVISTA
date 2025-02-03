from fastapi import APIRouter, HTTPException, Depends, Request
import requests
import pandas as pd
import json
import psycopg2
from typing import Dict, Any

chatbot_router = APIRouter()

class CompletionExecutor:
    def __init__(self):
        self._host = "https://clovastudio.stream.ntruss.com"
        self._api_key = "Bearer nv-f5786fde571f424786ed0823986ca992h3P1"
        self._request_id = "309fa53d16a64d7c9c2d8f67f74ac70d"

    def execute(self, prompt_type: str, metrics: Dict[str, Any], max_tokens: int = 2000):
        from prs_cns.prompt import (PROMPT_revenue, PROMPT_engagement, PROMPT_communication,
                                  PROMPT_targeting, PROMPT_popular_videos, PROMPT_thumbnail,
                                  PROMPT_upload_pattern, PROMPT_activity, PROMPT_summary)
        
        prompts = {
            'revenue': PROMPT_revenue,
            'engagement': PROMPT_engagement,
            'communication': PROMPT_communication,
            'targeting': PROMPT_targeting,
            'popular_videos': PROMPT_popular_videos,
            'thumbnail': PROMPT_thumbnail,
            'upload_pattern': PROMPT_upload_pattern,
            'activity': PROMPT_activity,
            'summary' : PROMPT_summary
        }
        
        prompt = prompts[prompt_type]
        formatted_prompt = [
            prompt[0],
            {"role": "user", "content": prompt[1]["content"].format(**metrics)}
        ]

        request_data = {
            "messages": formatted_prompt,
            "topP": 0.8,
            "maxTokens": max_tokens,
            "temperature": 0.15,
            "repeatPenalty": 5.0,
            "stopBefore": [],
            "includeAiFilters": False,
            "seed": 0,
        }

        headers = {
            "Authorization": self._api_key,
            "X-NCP-CLOVASTUDIO-REQUEST-ID": self._request_id,
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "text/event-stream",
        }
        
        response_content = ""
        with requests.post(
            self._host + "/testapp/v1/chat-completions/HCX-003", headers=headers, json=request_data, stream=True
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

conn = psycopg2.connect(host="10.28.224.177", port="30634", user="postgres", password="0104", database="postgres")
query = f"""
        SELECT "id", "title"
        FROM "Channel";
        """
with conn.cursor() as cur:
    id_df = pd.read_sql(query, conn)
    name_to_id = {name: int(id) for name, id in zip(id_df["title"].values, id_df["id"].values)}


###################
## 채널 수익성 API ##
###################
@chatbot_router.get("/profitability/revenue-analysis/{channel_name}")
async def analyze_revenue(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 채널 수익성 분석"""
    executor = CompletionExecutor()
    return executor.execute('revenue', metrics)

###################
## 시청자 관계 API ##
###################
@chatbot_router.get("/audience/engagement-analysis/{channel_name}")
async def analyze_engagement(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 시청자 참여도 분석"""
    try:
        # 채널의 구독자 수 범위 파악용 (경쟁 채널 비교를 위해)
        channel_info_query = f"""
            SELECT "subscriberCount"
            FROM public."Channel"
            WHERE "id" = '{name_to_id[channel_name]}'
        """
        channel_info = pd.read_sql(channel_info_query, db_engine)
        subscriber_count = channel_info.iloc[0]["subscriberCount"]

        # 현재 채널의 참여도 지표
        engagement_query = f"""
            SELECT 
                SUM(CAST(v."videoViewCount" AS INTEGER)) as total_views,
                SUM(CAST(v."videoLikeCount" AS INTEGER)) as total_likes,
                SUM(CAST(v."commentCount" AS INTEGER)) as total_comments,
                SUM(CAST(v."videoShareCount" AS INTEGER)) as total_shares
            FROM public."Video" v
            WHERE v."channel_id" = '{name_to_id[channel_name]}'
            AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
        """

        # 경쟁 채널들의 평균 참여도
        competitor_query = f"""
            WITH competitor_metrics AS (
                SELECT 
                    v.channel_id,
                    SUM(CAST(v."videoViewCount" AS INTEGER)) as total_views,
                    SUM(CAST(v."videoLikeCount" AS INTEGER)) as total_likes,
                    SUM(CAST(v."commentCount" AS INTEGER)) as total_comments,
                    SUM(CAST(v."videoShareCount" AS INTEGER)) as total_shares
                FROM public."Video" v
                JOIN public."Channel" c ON v.channel_id = c.id
                WHERE CAST(c."subscriberCount" AS INTEGER) 
                    BETWEEN CAST({subscriber_count} AS INTEGER) - 500000 
                    AND CAST({subscriber_count} AS INTEGER) + 500000
                AND v.channel_id != '{name_to_id[channel_name]}'
                AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY v.channel_id
            )
            SELECT 
                AVG((total_likes::float / NULLIF(total_views, 0)) * 100) as avg_like_ratio,
                AVG((total_comments::float / NULLIF(total_views, 0)) * 100) as avg_comment_ratio,
                AVG((total_shares::float / NULLIF(total_views, 0)) * 100) as avg_share_ratio
            FROM competitor_metrics
        """

        # 전체 순위
        rank_query = f"""
            WITH channel_metrics AS (
                SELECT 
                    channel_id,
                    SUM(CAST("videoLikeCount" AS FLOAT)) / NULLIF(SUM(CAST("videoViewCount" AS FLOAT)), 0) * 100 as engagement_rate
                FROM public."Video"
                WHERE CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY channel_id
            )
            SELECT 
                COUNT(*) + 1 as rank
            FROM channel_metrics
            WHERE engagement_rate > (
                SELECT engagement_rate 
                FROM channel_metrics 
                WHERE channel_id = '{name_to_id[channel_name]}'
            )
        """

        # 전체 채널 수
        total_channels_query = "SELECT COUNT(*) as total_channels FROM public.\"Channel\""

        # 겅쟁 채널 수, 순위
        similar_size_query = f"""
            WITH similar_channels AS (
                SELECT id
                FROM public."Channel"
                WHERE CAST("subscriberCount" AS INTEGER) 
                BETWEEN CAST({subscriber_count} AS INTEGER) - 500000 
                AND CAST({subscriber_count} AS INTEGER) + 500000
            )
            SELECT 
                COUNT(*) as similar_size_channels,
                (
                    SELECT COUNT(*) + 1
                    FROM similar_channels sc
                    JOIN (
                        SELECT 
                            v.channel_id,
                            SUM(CAST("videoLikeCount" AS FLOAT)) / NULLIF(SUM(CAST("videoViewCount" AS FLOAT)), 0) * 100 as engagement_rate
                        FROM public."Video" v
                        WHERE CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                        GROUP BY v.channel_id
                    ) vm ON vm.channel_id = sc.id
                    WHERE vm.engagement_rate > (
                        SELECT 
                            SUM(CAST("videoLikeCount" AS FLOAT)) / NULLIF(SUM(CAST("videoViewCount" AS FLOAT)), 0) * 100
                        FROM public."Video"
                        WHERE channel_id = '{name_to_id[channel_name]}'
                        AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                    )
                ) as similar_size_rank
            FROM similar_channels
        """

        # 쿼리 실행
        df = pd.read_sql(engagement_query, db_engine)
        competitor_df = pd.read_sql(competitor_query, db_engine)
        rank_df = pd.read_sql(rank_query, db_engine)
        total_channels_df = pd.read_sql(total_channels_query, db_engine)
        similar_size_df = pd.read_sql(similar_size_query, db_engine)

        # 데이터 추출
        total_views = float(df.iloc[0]["total_views"]) if df.iloc[0]["total_views"] is not None else 0
        total_likes = float(df.iloc[0]["total_likes"]) if df.iloc[0]["total_likes"] is not None else 0
        total_comments = float(df.iloc[0]["total_comments"]) if df.iloc[0]["total_comments"] is not None else 0
        total_shares = float(df.iloc[0]["total_shares"]) if df.iloc[0]["total_shares"] is not None else 0

        # metrics 구성
        metrics = {
            "like_ratio": round((total_likes / total_views * 100) if total_views > 0 else 0, 2),
            "comment_ratio": round((total_comments / total_views * 100) if total_views > 0 else 0, 2),
            "share_ratio": round((total_shares / total_views * 100) if total_views > 0 else 0, 2),
            "avg_like_ratio": round(competitor_df.iloc[0]["avg_like_ratio"], 2),
            "avg_comment_ratio": round(competitor_df.iloc[0]["avg_comment_ratio"], 2),
            "avg_share_ratio": round(competitor_df.iloc[0]["avg_share_ratio"], 2),
            "total_channels": int(total_channels_df.iloc[0]["total_channels"]),
            "engagement_rank": int(rank_df.iloc[0]["rank"]),
            "similar_size_channels": int(similar_size_df.iloc[0]["similar_size_channels"]),
            "similar_size_rank": int(similar_size_df.iloc[0]["similar_size_rank"])
        }

        executor = CompletionExecutor()
        return executor.execute('engagement', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chatbot_router.get("/audience/communication-analysis/{channel_name}")
async def analyze_communication(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 크리에이터 소통 분석"""
    executor = CompletionExecutor()
    return executor.execute('communication', metrics)

@chatbot_router.get("/audience/targeting-analysis/{channel_name}")
async def analyze_targeting(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 시청자 타겟팅 분석"""
    executor = CompletionExecutor()
    return executor.execute('targeting', metrics)


###################
## 채널 성과 API ##
###################
@chatbot_router.get("/performance/popular-videos-analysis/{channel_name}")
async def analyze_popular_videos(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 인기 영상 분석"""
    executor = CompletionExecutor()
    return executor.execute('popular_videos', metrics)

@chatbot_router.get("/performance/thumbnail-analysis/{channel_name}")
async def analyze_thumbnails(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 썸네일 성과 분석"""
    executor = CompletionExecutor()
    return executor.execute('thumbnail', metrics)

@chatbot_router.get("/performance/upload-pattern-analysis/{channel_name}")
async def analyze_upload_pattern(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 업로드 주기 분석"""
    executor = CompletionExecutor()
    return executor.execute('upload_pattern', metrics)

@chatbot_router.get("/performance/activity-analysis/{channel_name}")
async def analyze_activity(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 채널 활성도 분석"""
    executor = CompletionExecutor()
    return executor.execute('activity', metrics)

@chatbot_router.get("/summary/{channel_name}")
async def analyze_channel_summary(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    모든 분석 결과를 종합하여 3줄 요약을 반환합니다.
    """
    try:
        # 수익성 데이터 쿼리
        revenue_query = f"""
        SELECT 
            "viewCount",
            (SELECT AVG(CAST("viewCount" as float)) FROM "Channel") as avg_viewcount
        FROM public."Channel"
        WHERE "id" = '{name_to_id[channel_name]}'
        """
        
        df = pd.read_sql(revenue_query, db_engine)

        viewcount = int(df.iloc[0]["viewCount"])
        avg_viewcount = int(df.iloc[0]["avg_viewcount"])

        view_income = int((viewcount * 2 + viewcount * 4.5) / 2)

        metrics = {
            'view_income': view_income
        }
        
        content = PROMPT_summary[1]['content'].format(**metrics)
        executor = CompletionExecutor()
        return executor.execute('summary', metrics)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))