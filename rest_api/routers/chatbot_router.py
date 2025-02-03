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
    try:
        # 채널 구독자 수 확인 (경쟁 채널 범위 설정용)
        channel_info_query = f"""
            SELECT 
                CAST("subscriberCount" AS INTEGER) as "subscriberCount",
                "DisplayName"
            FROM public."Channel"
            WHERE "id" = '{name_to_id[channel_name]}'
        """
        channel_info = pd.read_sql(channel_info_query, db_engine)
        subscriber_count = channel_info.iloc[0]["subscriberCount"]
        display_name = channel_info.iloc[0]["DisplayName"]

        # 라이브 방송 관련 데이터
        live_query = f"""
            SELECT 
                CAST("LiveBroadcastingCount" AS INTEGER) as live_count,
                CAST("LiveBroadcastingViewer" AS INTEGER) as live_viewers
            FROM public."Channel"
            WHERE "id" = '{name_to_id[channel_name]}'
        """

        # 경쟁 채널들의 라이브 방송 평균
        competitor_live_query = f"""
            SELECT COALESCE(AVG(CAST("LiveBroadcastingCount" AS FLOAT)), 0) as avg_competitor_live
            FROM public."Channel"
            WHERE CAST("subscriberCount" AS INTEGER) 
                BETWEEN {subscriber_count} - 500000 AND {subscriber_count} + 500000
            AND "id" != '{name_to_id[channel_name]}'
        """

        # 크리에이터 댓글 수
        reply_query = f"""
            SELECT COUNT(*) as reply_count
            FROM public."Video" v
            JOIN public."Comments" c ON c."vId" = v."vId"
            WHERE v."channel_id" = '{name_to_id[channel_name]}'
            AND strpos(c."replies", '@{display_name}') > 0
        """

        # 경쟁 채널들의 평균 댓글 수
        competitor_replies_query = f"""
            SELECT COALESCE(AVG(reply_count), 0) as avg_competitor_replies
            FROM (
                SELECT 
                    ch."id",
                    COUNT(*) as reply_count
                FROM public."Channel" ch
                JOIN public."Video" v ON v."channel_id" = ch."id"
                JOIN public."Comments" cm ON cm."vId" = v."vId"
                    AND strpos(cm."replies", '@' || ch."DisplayName") > 0
                WHERE CAST(ch."subscriberCount" AS INTEGER)
                    BETWEEN {subscriber_count} - 500000 AND {subscriber_count} + 500000
                AND ch."id" != '{name_to_id[channel_name]}'
                GROUP BY ch."id"
            ) subquery
        """

        # 순위 쿼리 (라이브 방송 기준)
        live_rank_query = f"""
            SELECT COUNT(*) + 1 as live_rank
            FROM public."Channel"
            WHERE CAST("LiveBroadcastingCount" AS INTEGER) > (
                SELECT CAST("LiveBroadcastingCount" AS INTEGER)
                FROM public."Channel"
                WHERE "id" = '{name_to_id[channel_name]}'
            )
        """

        # 댓글 순위 쿼리
        reply_rank_query = f"""
            WITH reply_counts AS (
                SELECT 
                    ch."id",
                    COUNT(*) as reply_count
                FROM public."Channel" ch
                JOIN public."Video" v ON v."channel_id" = ch."id"
                JOIN public."Comments" cm ON cm."vId" = v."vId"
                    AND strpos(cm."replies", '@' || ch."DisplayName") > 0
                GROUP BY ch."id"
            )
            SELECT COUNT(*) + 1 as reply_rank
            FROM reply_counts
            WHERE reply_count > (
                SELECT reply_count
                FROM reply_counts
                WHERE "id" = '{name_to_id[channel_name]}'
            )
        """

        # 유사 규모 채널 수와 순위 쿼리
        similar_size_query = f"""
            SELECT COUNT(*) as similar_size_channels
            FROM public."Channel"
            WHERE CAST("subscriberCount" AS INTEGER)
                BETWEEN {subscriber_count} - 500000 AND {subscriber_count} + 500000
        """
        total_channels_query = "SELECT COUNT(*) as total_channels FROM public.\"Channel\""

        total_channels_df = pd.read_sql(total_channels_query, db_engine)

        # 쿼리 실행
        live_df = pd.read_sql(live_query, db_engine)
        competitor_live_df = pd.read_sql(competitor_live_query, db_engine)
        reply_df = pd.read_sql(reply_query, db_engine)
        competitor_replies_df = pd.read_sql(competitor_replies_query, db_engine)
        live_rank_df = pd.read_sql(live_rank_query, db_engine)
        reply_rank_df = pd.read_sql(reply_rank_query, db_engine)
        similar_size_df = pd.read_sql(similar_size_query, db_engine)
        
        metrics = {
            "live_count": int(live_df.iloc[0]["live_count"]) if not live_df.empty and live_df.iloc[0]["live_count"] is not None else 0,
            "live_rank": int(live_rank_df.iloc[0]["live_rank"]) if not live_rank_df.empty and live_rank_df.iloc[0]["live_rank"] is not None else 0,
            "avg_competitor_live": round(float(competitor_live_df.iloc[0]["avg_competitor_live"]), 1) if not competitor_live_df.empty and competitor_live_df.iloc[0]["avg_competitor_live"] is not None else 0,
            "live_viewers": int(live_df.iloc[0]["live_viewers"]) if not live_df.empty and live_df.iloc[0]["live_viewers"] is not None else 0,
            "reply_count": int(reply_df.iloc[0]["reply_count"]) if not reply_df.empty and reply_df.iloc[0]["reply_count"] is not None else 0,
            "reply_rank": int(reply_rank_df.iloc[0]["reply_rank"]) if not reply_rank_df.empty and reply_rank_df.iloc[0]["reply_rank"] is not None else 0,
            "avg_competitor_replies": int(competitor_replies_df.iloc[0]["avg_competitor_replies"]) if not competitor_replies_df.empty and competitor_replies_df.iloc[0]["avg_competitor_replies"] is not None else 0,
            "similar_size_channels": int(similar_size_df.iloc[0]["similar_size_channels"]) if not similar_size_df.empty and similar_size_df.iloc[0]["similar_size_channels"] is not None else 0,
            "live_similar_rank": int(live_rank_df.iloc[0]["live_rank"]) if not live_rank_df.empty and live_rank_df.iloc[0]["live_rank"] is not None else 0,
            "reply_similar_rank": int(reply_rank_df.iloc[0]["reply_rank"]) if not reply_rank_df.empty and reply_rank_df.iloc[0]["reply_rank"] is not None else 0,
            "total_channels": int(total_channels_df.iloc[0]["total_channels"]) if not total_channels_df.empty and total_channels_df.iloc[0]["total_channels"] is not None else 0  # 추가
        }

        executor = CompletionExecutor()
        return executor.execute('communication', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chatbot_router.get("/audience/targeting-analysis/{channel_name}")
async def analyze_targeting(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 시청자 타겟팅 분석"""
    try:
        # 키워드 추출 (태그와 설명의 해시태그)
        keyword_query = f"""
            SELECT 
                v.tags,
                v."videoDescription"
            FROM public."Video" v
            WHERE v."channel_id" = '{name_to_id[channel_name]}'
            AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
        """
        
        # 업로드 시간대
        upload_time_query = f"""
            SELECT 
                SUBSTRING(v."videoPublishedAt", 12, 2) AS upload_hour,
                COUNT(*) as upload_count
            FROM public."Video" v
            WHERE v."channel_id" = '{name_to_id[channel_name]}'
            AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
            GROUP BY upload_hour
            ORDER BY upload_count DESC
            LIMIT 3
        """

        # 시청 시간대 (댓글 시간 기준)
        view_time_query = f"""
            SELECT 
                SUBSTRING(c."commentPublishedAt", 12, 2) AS view_hour,
                COUNT(*) AS comment_count
            FROM public."Comments" c
            JOIN public."Video" v ON c."vId" = v."vId"
            WHERE v."channel_id" = '{name_to_id[channel_name]}'
            AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
            GROUP BY view_hour
            ORDER BY comment_count DESC
            LIMIT 3
        """

        # 업로드 수와 순위
        upload_stats_query = f"""
            WITH upload_counts AS (
                SELECT 
                    channel_id,
                    COUNT(*) as upload_count
                FROM public."Video"
                WHERE CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY channel_id
            )
            SELECT 
                (SELECT upload_count FROM upload_counts WHERE channel_id = '{name_to_id[channel_name]}') as upload_count,
                (
                    SELECT COUNT(*) + 1
                    FROM upload_counts
                    WHERE upload_count > (
                        SELECT upload_count 
                        FROM upload_counts 
                        WHERE channel_id = '{name_to_id[channel_name]}'
                    )
                ) as upload_rank
        """

        # 광고 영상 비율
        ad_ratio_query = f"""
            WITH channel_ratios AS (
                SELECT 
                    channel_id,
                    CAST(SUM(CASE WHEN "hasPaidProductPlacement" = true THEN 1 ELSE 0 END) AS FLOAT) / 
                    CAST(COUNT(*) AS FLOAT) * 100 as ad_ratio
                FROM public."Video"
                GROUP BY channel_id
            )
            SELECT 
                (SELECT ad_ratio FROM channel_ratios WHERE channel_id = '{name_to_id[channel_name]}') as ad_ratio,
                (SELECT AVG(ad_ratio) FROM channel_ratios) as avg_ad_ratio,
                (
                    SELECT COUNT(*) + 1
                    FROM channel_ratios
                    WHERE ad_ratio > (
                        SELECT ad_ratio 
                        FROM channel_ratios 
                        WHERE channel_id = '{name_to_id[channel_name]}'
                    )
                ) as ad_ratio_rank
        """

        # 전체 채널 수
        total_channels_query = "SELECT COUNT(*) as total_channels FROM public.\"Channel\""

        keyword_df = pd.read_sql(keyword_query, db_engine)
        upload_time_df = pd.read_sql(upload_time_query, db_engine)
        view_time_df = pd.read_sql(view_time_query, db_engine)
        upload_stats_df = pd.read_sql(upload_stats_query, db_engine)
        ad_ratio_df = pd.read_sql(ad_ratio_query, db_engine)
        total_channels_df = pd.read_sql(total_channels_query, db_engine)

        # 키워드 추출 및 처리
        all_keywords = []
        for tags in keyword_df["tags"]:
            if tags:
                all_keywords.extend(
                    [tag.strip("#").strip("{}").lower().replace('"', "").replace("\\", "").replace("\n", "")
                     for tag in tags.split(",")]
                )
        for desc in keyword_df["videoDescription"]:
            if desc:
                all_keywords.extend(
                    [word.strip("#").lower().replace('"', "").replace("\\", "").replace("\n", "")
                     for word in desc.split("#")
                     if word.strip()]
                )
        
        from collections import Counter
        keyword_counts = Counter(all_keywords)
        top_keywords = [k for k, v in keyword_counts.most_common(10) if len(k) < 15]

        metrics = {
            "keywords": ", ".join(top_keywords),
            "upload_times": ", ".join([f"{h}시" for h in upload_time_df["upload_hour"].tolist()]) if not upload_time_df.empty else "",
            "viewing_times": ", ".join([f"{h}시" for h in view_time_df["view_hour"].tolist()]) if not view_time_df.empty else "",
            "upload_count": int(upload_stats_df.iloc[0]["upload_count"]) if not upload_stats_df.empty and upload_stats_df.iloc[0]["upload_count"] is not None else 0,
            "total_channels": int(total_channels_df.iloc[0]["total_channels"]) if not total_channels_df.empty and total_channels_df.iloc[0]["total_channels"] is not None else 0,
            "ad_ratio": float(ad_ratio_df.iloc[0]["ad_ratio"]) if not ad_ratio_df.empty and ad_ratio_df.iloc[0]["ad_ratio"] is not None else 0,
            "avg_ad_ratio": float(ad_ratio_df.iloc[0]["avg_ad_ratio"]) if not ad_ratio_df.empty and ad_ratio_df.iloc[0]["avg_ad_ratio"] is not None else 0,
            "ad_ratio_rank": int(ad_ratio_df.iloc[0]["ad_ratio_rank"]) if not ad_ratio_df.empty and ad_ratio_df.iloc[0]["ad_ratio_rank"] is not None else 0,
            "upload_rank": int(upload_stats_df.iloc[0]["upload_rank"]) if not upload_stats_df.empty and upload_stats_df.iloc[0]["upload_rank"] is not None else 0
        }

        executor = CompletionExecutor()
        return executor.execute('targeting', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


###################
## 채널 성과 API ##
###################
@chatbot_router.get("/performance/popular-videos-analysis/{channel_name}")
async def analyze_popular_videos(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 인기 영상 분석"""
    try:
        # 인기 영상 쿼리
        popular_videos_query = f"""
            WITH video_metrics AS (
                SELECT 
                    "videoTitle" as title,
                    "videoThumbnails" as thumbnail,
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    CAST("videoAPV" AS FLOAT) as retention_rate,
                    CAST(("commentCount"::FLOAT / NULLIF("videoViewCount"::FLOAT, 0) * 100) as FLOAT) as comment_rate,
                    CAST(("videoLikeCount"::FLOAT / NULLIF("videoViewCount"::FLOAT, 0) * 100) as FLOAT) as like_rate,
                    CAST("videoCTR" AS FLOAT) as ctr,
                    CAST("videoViewCount" AS FLOAT) / (
                        SELECT AVG(CAST("videoViewCount" AS FLOAT))
                        FROM public."Video"
                        WHERE "channel_id" = '{name_to_id[channel_name]}'
                        AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                    ) as view_ratio
                FROM public."Video"
                WHERE "channel_id" = '{name_to_id[channel_name]}'
                AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
            )
            SELECT *
            FROM video_metrics
            ORDER BY view_count DESC
            LIMIT 3
        """

        # 쿼리 실행
        df = pd.read_sql(popular_videos_query, db_engine)
        
        # metrics 구성
        metrics = {
            # 첫 번째 영상
            "title1": df.iloc[0]["title"] if not df.empty else "",
            #"thumbnail1": df.iloc[0]["thumbnail"] if not df.empty else "",
            "view_count1": float(df.iloc[0]["view_count"]) if not df.empty and df.iloc[0]["view_count"] is not None else 0,
            "retention_rate1": float(df.iloc[0]["retention_rate"]) if not df.empty and df.iloc[0]["retention_rate"] is not None else 0,
            "comment_rate1": float(df.iloc[0]["comment_rate"]) if not df.empty and df.iloc[0]["comment_rate"] is not None else 0,
            "like_rate1": float(df.iloc[0]["like_rate"]) if not df.empty and df.iloc[0]["like_rate"] is not None else 0,
            "ctr1": float(df.iloc[0]["ctr"]) if not df.empty and df.iloc[0]["ctr"] is not None else 0,
            "view_ratio1": float(df.iloc[0]["view_ratio"]) if not df.empty and df.iloc[0]["view_ratio"] is not None else 0,

            # 두 번째 영상
            "title2": df.iloc[1]["title"] if len(df) > 1 else "",
            #"thumbnail2": df.iloc[1]["thumbnail"] if len(df) > 1 else "",
            "view_count2": float(df.iloc[1]["view_count"]) if len(df) > 1 and df.iloc[1]["view_count"] is not None else 0,
            "retention_rate2": float(df.iloc[1]["retention_rate"]) if len(df) > 1 and df.iloc[1]["retention_rate"] is not None else 0,
            "comment_rate2": float(df.iloc[1]["comment_rate"]) if len(df) > 1 and df.iloc[1]["comment_rate"] is not None else 0,
            "like_rate2": float(df.iloc[1]["like_rate"]) if len(df) > 1 and df.iloc[1]["like_rate"] is not None else 0,
            "ctr2": float(df.iloc[1]["ctr"]) if len(df) > 1 and df.iloc[1]["ctr"] is not None else 0,
            "view_ratio2": float(df.iloc[1]["view_ratio"]) if len(df) > 1 and df.iloc[1]["view_ratio"] is not None else 0,

            # 세 번째 영상
            "title3": df.iloc[2]["title"] if len(df) > 2 else "",
            #"thumbnail3": df.iloc[2]["thumbnail"] if len(df) > 2 else "",
            "view_count3": float(df.iloc[2]["view_count"]) if len(df) > 2 and df.iloc[2]["view_count"] is not None else 0,
            "retention_rate3": float(df.iloc[2]["retention_rate"]) if len(df) > 2 and df.iloc[2]["retention_rate"] is not None else 0,
            "comment_rate3": float(df.iloc[2]["comment_rate"]) if len(df) > 2 and df.iloc[2]["comment_rate"] is not None else 0,
            "like_rate3": float(df.iloc[2]["like_rate"]) if len(df) > 2 and df.iloc[2]["like_rate"] is not None else 0,
            "ctr3": float(df.iloc[2]["ctr"]) if len(df) > 2 and df.iloc[2]["ctr"] is not None else 0,
            "view_ratio3": float(df.iloc[2]["view_ratio"]) if len(df) > 2 and df.iloc[2]["view_ratio"] is not None else 0
        }

        executor = CompletionExecutor()
        return executor.execute('popular_videos', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chatbot_router.get("/performance/thumbnail-analysis/{channel_name}")
async def analyze_thumbnails(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 썸네일 성과 분석"""
    try:
        # 썸네일 성과 쿼리
        thumbnail_query = f"""
            WITH thumbnail_metrics AS (
                SELECT 
                    "videoTitle" as title,
                    "videoThumbnails" as thumbnail,
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    CAST("videoAPV" AS FLOAT) as apv,
                    CAST(("commentCount"::FLOAT / NULLIF("videoViewCount"::FLOAT, 0) * 100) as FLOAT) as comment_rate,
                    CAST(("videoLikeCount"::FLOAT / NULLIF("videoViewCount"::FLOAT, 0) * 100) as FLOAT) as like_rate,
                    CAST("videoCTR" AS FLOAT) as ctr,
                    CAST("videoCTR" AS FLOAT) / (
                        SELECT AVG(CAST("videoCTR" AS FLOAT))
                        FROM public."Video"
                        WHERE "channel_id" = '{name_to_id[channel_name]}'
                        AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                    ) as ctr_ratio
                FROM public."Video"
                WHERE "channel_id" = '{name_to_id[channel_name]}'
                AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
            )
            SELECT *
            FROM thumbnail_metrics
            ORDER BY ctr DESC, apv DESC
            LIMIT 3
        """

        df = pd.read_sql(thumbnail_query, db_engine)
        
        metrics = {
            # 첫 번째 썸네일
            "title1": df.iloc[0]["title"] if not df.empty else "",
            #"thumbnail1": df.iloc[0]["thumbnail"] if not df.empty else "",
            "view_count1": float(df.iloc[0]["view_count"]) if not df.empty and df.iloc[0]["view_count"] is not None else 0,
            "retention_rate1": float(df.iloc[0]["apv"]) if not df.empty and df.iloc[0]["apv"] is not None else 0,
            "comment_rate1": float(df.iloc[0]["comment_rate"]) if not df.empty and df.iloc[0]["comment_rate"] is not None else 0,
            "like_rate1": float(df.iloc[0]["like_rate"]) if not df.empty and df.iloc[0]["like_rate"] is not None else 0,
            "ctr1": float(df.iloc[0]["ctr"]) if not df.empty and df.iloc[0]["ctr"] is not None else 0,
            "ctr_ratio1": float(df.iloc[0]["ctr_ratio"]) if not df.empty and df.iloc[0]["ctr_ratio"] is not None else 0,

            # 두 번째 썸네일
            "title2": df.iloc[1]["title"] if len(df) > 1 else "",
            #"thumbnail2": df.iloc[1]["thumbnail"] if len(df) > 1 else "",
            "view_count2": float(df.iloc[1]["view_count"]) if len(df) > 1 and df.iloc[1]["view_count"] is not None else 0,
            "retention_rate2": float(df.iloc[1]["apv"]) if len(df) > 1 and df.iloc[1]["apv"] is not None else 0,
            "comment_rate2": float(df.iloc[1]["comment_rate"]) if len(df) > 1 and df.iloc[1]["comment_rate"] is not None else 0,
            "like_rate2": float(df.iloc[1]["like_rate"]) if len(df) > 1 and df.iloc[1]["like_rate"] is not None else 0,
            "ctr2": float(df.iloc[1]["ctr"]) if len(df) > 1 and df.iloc[1]["ctr"] is not None else 0,
            "ctr_ratio2": float(df.iloc[1]["ctr_ratio"]) if len(df) > 1 and df.iloc[1]["ctr_ratio"] is not None else 0,

            # 세 번째 썸네일
            "title3": df.iloc[2]["title"] if len(df) > 2 else "",
            #"thumbnail3": df.iloc[2]["thumbnail"] if len(df) > 2 else "",
            "view_count3": float(df.iloc[2]["view_count"]) if len(df) > 2 and df.iloc[2]["view_count"] is not None else 0,
            "retention_rate3": float(df.iloc[2]["apv"]) if len(df) > 2 and df.iloc[2]["apv"] is not None else 0,
            "comment_rate3": float(df.iloc[2]["comment_rate"]) if len(df) > 2 and df.iloc[2]["comment_rate"] is not None else 0,
            "like_rate3": float(df.iloc[2]["like_rate"]) if len(df) > 2 and df.iloc[2]["like_rate"] is not None else 0,
            "ctr3": float(df.iloc[2]["ctr"]) if len(df) > 2 and df.iloc[2]["ctr"] is not None else 0,
            "ctr_ratio3": float(df.iloc[2]["ctr_ratio"]) if len(df) > 2 and df.iloc[2]["ctr_ratio"] is not None else 0
        }

        executor = CompletionExecutor()
        return executor.execute('thumbnail', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chatbot_router.get("/performance/upload-pattern-analysis/{channel_name}")
async def analyze_upload_pattern(channel_name: str, db_engine=Depends(get_db_engine)):
    """CLOVA X를 이용한 업로드 주기 분석"""
    try:
        # 채널의 구독자 수 범위 파악용 (경쟁 채널 비교를 위해)
        channel_info_query = f"""
            SELECT "subscriberCount"
            FROM public."Channel"
            WHERE "id" = '{name_to_id[channel_name]}'
        """
        channel_info = pd.read_sql(channel_info_query, db_engine)
        subscriber_count = channel_info.iloc[0]["subscriberCount"]

        # 월별 업로드 추이 (최근 12개월)
        monthly_query = f"""
            SELECT 
                TO_CHAR(DATE_TRUNC('month', CAST("videoPublishedAt" AS DATE)), 'YYYY-MM') AS month,
                COUNT(*) AS videocount
            FROM public."Video"
            WHERE CAST("videoPublishedAt" AS DATE) >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '11 months'
            AND "channel_id" = '{name_to_id[channel_name]}'
            GROUP BY month
            ORDER BY month;
        """

        # 전체 영상 수와 월평균 업로드
        video_stats_query = f"""
            SELECT 
                COUNT(*) as total_videos,
                COUNT(*) / 12.0 as monthly_avg
            FROM public."Video"
            WHERE "channel_id" = '{name_to_id[channel_name]}'
            AND CAST("videoPublishedAt" AS DATE) >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '11 months'
        """

        # 업로드 순위 (전체 채널 중)
        upload_rank_query = f"""
            WITH channel_uploads AS (
                SELECT 
                    channel_id,
                    COUNT(*) as upload_count
                FROM public."Video"
                WHERE CAST("videoPublishedAt" AS DATE) >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '11 months'
                GROUP BY channel_id
            )
            SELECT COUNT(*) + 1 as rank
            FROM channel_uploads
            WHERE upload_count > (
                SELECT upload_count
                FROM channel_uploads
                WHERE channel_id = '{name_to_id[channel_name]}'
            )
        """

        # 채널 참여도와 평균
        engagement_query = f"""
            SELECT AVG("subscriberViewedRatio") as participation
            FROM "Video"
            WHERE "channel_id" = '{name_to_id[channel_name]}'
            AND CAST("videoPublishedAt" AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
        """

        # 경쟁 채널 평균 참여율
        competitor_engagement_query = f"""
            WITH competitor_participation AS (
                SELECT 
                    v.channel_id,
                    AVG("subscriberViewedRatio") as channel_participation
                FROM "Video" v
                JOIN "Channel" c ON v.channel_id = c.id
                WHERE CAST(c."subscriberCount" AS INTEGER) 
                    BETWEEN CAST({subscriber_count} AS INTEGER) - 500000 
                    AND CAST({subscriber_count} AS INTEGER) + 500000
                AND v.channel_id != '{name_to_id[channel_name]}'
                AND CAST(v."videoPublishedAt" AS DATE) >= CURRENT_DATE - INTERVAL '90 days'
                GROUP BY v.channel_id
            )
            SELECT AVG(channel_participation) as avg_participation
            FROM competitor_participation
        """

        monthly_df = pd.read_sql(monthly_query, db_engine)
        video_stats_df = pd.read_sql(video_stats_query, db_engine)
        upload_rank_df = pd.read_sql(upload_rank_query, db_engine)
        engagement_df = pd.read_sql(engagement_query, db_engine)
        competitor_engagement_df = pd.read_sql(competitor_engagement_query, db_engine)

        total_channels_query = "SELECT COUNT(*) as total_channels FROM public.\"Channel\""
        total_channels_df = pd.read_sql(total_channels_query, db_engine)

        metrics = {
            "monthly_data": monthly_df.to_dict('records'),
            "monthly_uploads": round(float(video_stats_df.iloc[0]["monthly_avg"]) if video_stats_df.iloc[0]["monthly_avg"] is not None else 0, 1),
            "video_count": int(video_stats_df.iloc[0]["total_videos"]) if video_stats_df.iloc[0]["total_videos"] is not None else 0,
            "upload_rank": int(upload_rank_df.iloc[0]["rank"]) if upload_rank_df.iloc[0]["rank"] is not None else 0,
            "participation": round(float(engagement_df.iloc[0]["participation"]) if engagement_df.iloc[0]["participation"] is not None else 0, 1),
            "engagement_rank": int(upload_rank_df.iloc[0]["rank"]) if upload_rank_df.iloc[0]["rank"] is not None else 0,
            "avg_participation": round(float(competitor_engagement_df.iloc[0]["avg_participation"]) if competitor_engagement_df.iloc[0]["avg_participation"] is not None else 0, 1),
            "total_channels": int(total_channels_df.iloc[0]["total_channels"]) if total_channels_df.iloc[0]["total_channels"] is not None else 0
        }

        executor = CompletionExecutor()
        return executor.execute('upload_pattern', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@chatbot_router.get("/performance/activity-analysis/{channel_name}")
async def analyze_activity(channel_name: str, db_engine=Depends(get_db_engine)):
    try:
        # 채널 기본 정보 조회 (구독자 수)
        channel_info_query = f"""
            SELECT CAST("subscriberCount" AS INTEGER) as "subscriberCount"
            FROM public."Channel"
            WHERE "id" = '{name_to_id[channel_name]}'
        """
        channel_info = pd.read_sql(channel_info_query, db_engine)
        subscriber_count = channel_info.iloc[0]["subscriberCount"]

        # 채널 평균 조회수 및 순위
        view_stats_query = f"""
            WITH channel_views AS (
                SELECT 
                    channel_id,
                    CAST(AVG(CAST("videoViewCount" AS FLOAT)) AS FLOAT) as avg_views
                FROM public."Video"
                WHERE CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY channel_id
            )
            SELECT 
                CAST(avg_views AS FLOAT) as avg_views,
                (
                    SELECT COUNT(*) + 1
                    FROM channel_views v2
                    WHERE CAST(v2.avg_views AS FLOAT) > CAST((
                        SELECT avg_views
                        FROM channel_views 
                        WHERE channel_id = '{name_to_id[channel_name]}'
                    ) AS FLOAT)
                ) as view_rank
            FROM channel_views
            WHERE channel_id = '{name_to_id[channel_name]}'
        """

        # 경쟁 채널 평균 조회수
        competitor_query = f"""
            SELECT AVG(avg_views) as competitor_avg_view
            FROM (
                SELECT 
                    v.channel_id,
                    AVG(CAST(v."videoViewCount" AS FLOAT)) as avg_views
                FROM public."Video" v
                JOIN public."Channel" c ON v.channel_id = c.id
                WHERE CAST(c."subscriberCount" AS INTEGER)
                    BETWEEN CAST({subscriber_count} AS INTEGER) - 500000 
                    AND CAST({subscriber_count} AS INTEGER) + 500000
                AND v.channel_id != '{name_to_id[channel_name]}'
                AND CAST(v."videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY v.channel_id
            ) competitor_views
        """

        # 월평균 업로드 수
        upload_query = f"""
            SELECT CAST(COUNT(*) AS FLOAT) / 3.0 as monthly_upload_count
            FROM public."Video"
            WHERE channel_id = '{name_to_id[channel_name]}'
            AND CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
        """

        # 구독자 참여도 및 순위
        engagement_query = f"""
            WITH channel_engagement AS (
                SELECT 
                    channel_id,
                    CAST(AVG(CAST("subscriberViewedRatio" AS FLOAT)) AS FLOAT) as engagement_rate
                FROM public."Video"
                WHERE CAST("videoPublishedAt" AS TIMESTAMP) >= NOW() - INTERVAL '90 days'
                GROUP BY channel_id
            )
            SELECT 
                CAST((
                    SELECT engagement_rate 
                    FROM channel_engagement 
                    WHERE channel_id = '{name_to_id[channel_name]}'
                ) AS FLOAT) as engagement_rate,
                (
                    SELECT COUNT(*) + 1
                    FROM channel_engagement
                    WHERE CAST(engagement_rate AS FLOAT) > CAST((
                        SELECT engagement_rate
                        FROM channel_engagement
                        WHERE channel_id = '{name_to_id[channel_name]}'
                    ) AS FLOAT)
                ) as engagement_rank
        """

        # 전체 채널 수
        total_channels_query = "SELECT COUNT(*) as total_channels FROM public.\"Channel\""

        # 쿼리 실행
        view_stats_df = pd.read_sql(view_stats_query, db_engine)
        competitor_df = pd.read_sql(competitor_query, db_engine)
        upload_df = pd.read_sql(upload_query, db_engine)
        engagement_df = pd.read_sql(engagement_query, db_engine)
        total_channels_df = pd.read_sql(total_channels_query, db_engine)

        # metrics 구성
        metrics = {
            "user_avg_view": float(view_stats_df.iloc[0]["avg_views"]) if not view_stats_df.empty and view_stats_df.iloc[0]["avg_views"] is not None else 0,
            "view_rank": int(view_stats_df.iloc[0]["view_rank"]) if not view_stats_df.empty and view_stats_df.iloc[0]["view_rank"] is not None else 0,
            "competitor_avg_view": float(competitor_df.iloc[0]["competitor_avg_view"]) if not competitor_df.empty and competitor_df.iloc[0]["competitor_avg_view"] is not None else 0,
            "view_subscriber_ratio": round((float(view_stats_df.iloc[0]["avg_views"]) / subscriber_count * 100) if not view_stats_df.empty and subscriber_count > 0 and view_stats_df.iloc[0]["avg_views"] is not None else 0, 1),
            "monthly_upload_count": round(float(upload_df.iloc[0]["monthly_upload_count"]) if not upload_df.empty and upload_df.iloc[0]["monthly_upload_count"] is not None else 0, 1),
            "engagement_rate": round(float(engagement_df.iloc[0]["engagement_rate"]) if not engagement_df.empty and engagement_df.iloc[0]["engagement_rate"] is not None else 0, 1),
            "engagement_rank": int(engagement_df.iloc[0]["engagement_rank"]) if not engagement_df.empty and engagement_df.iloc[0]["engagement_rank"] is not None else 0,
            "total_channels": int(total_channels_df.iloc[0]["total_channels"]) if not total_channels_df.empty and total_channels_df.iloc[0]["total_channels"] is not None else 0
        }

        executor = CompletionExecutor()
        return executor.execute('activity', metrics, max_tokens=300)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

###################
## SWOT 요약약 API ##
###################
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