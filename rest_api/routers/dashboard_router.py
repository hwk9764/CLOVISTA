from fastapi import APIRouter, HTTPException, Depends, Request
import pandas as pd
import psycopg2
from collections import Counter

dashboard_router = APIRouter()

def get_db_engine(request: Request):
    """
    FastAPI의 상태 객체에서 DB 엔진을 가져옵니다.
    """
    return request.app.state.db_engine

conn = psycopg2.connect(
        host="10.28.224.177",
        port="30634",
        user="postgres",
        password="0104",
        database="postgres"
    )
query = f"""
        SELECT "id", "name"
        FROM "Channel";
        """
with conn.cursor() as cur:
    id_df = pd.read_sql(query, conn)
    id_name_pair = {name:int(id) for name, id in zip(id_df['name'].values, id_df['id'].values)}

###################
## 채널 수익성 API ##
###################
@dashboard_router.get("/profitability/views-and-donations/{channel_name}")
async def get_views_and_donations(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    조회수 수입 및 후원 수입 데이터를 반환(조회수 수입, 슈퍼챗 및 후원 금액)
    Parameters:
        Channel_name: 유튜브 채널명 (나중에 채널 ID로 변경해야할 것 같음)
    Returns:
        [
            {"조회수_유저": 1,115,132},
            {"조회수_평균": 1,000,000},
            {"후원_유저": 568,186},
            {"후원_평균": 123,456}
        ]
    """

    # 코드 테스트할 때는 try, except 빼는 것을 추천
    try:
        channel_query = f"""
        SELECT "viewCount", "Donation",
            (SELECT AVG(CAST("viewCount" as float)) FROM "Channel") as avg_viewcount,
            (SELECT AVG(CAST("Donation" as float)) FROM "Channel") as avg_donation
        FROM public."Channel"
        WHERE "id" = '{id_name_pair[channel_name]}'
        """
        df = pd.read_sql(channel_query, db_engine)

        # 전처리 코드 추가
        viewcount = int(df.iloc[0]['viewCount'])
        avg_viewcount = int(df.iloc[0]['avg_viewcount'])
        view_profit_user = (viewcount*2, int(viewcount*4.5))
        view_profit_avg = (avg_viewcount*2, int(avg_viewcount*4.5))
        #donation_profit_user = int(df.iloc[0]['Donation'])
        #donation_profit_avg = int(df.iloc[0]['avg_donation'])

    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return [{
        "조회수_유저": view_profit_user,
        "조회수_평균": view_profit_avg,
        #"후원_유저": donation_profit_user,
        #"후원_평균": donation_profit_avg
        }]

@dashboard_router.get("/profitability/ad-video-status/{channel_name}")
async def get_ad_video_status(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    광고 영상 현황 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명 (나중에 채널 ID로 변경해야할 것 같음)
    Returns:
        [
            {"광고영상": "35개 (8달 전 업데이트)", "누적 재생": "1.2천만 (영상당 평균 ~~)", "누적 좋아요": "33.8만 (영상당 평균 ~~)", "누적 댓글": "7천만 (영상당 평균 ~~~)"}
        ]

    """
    def simplify(value):
        if value>=int(1e8): return f"{round(value/int(1e8), 1)}억"
        elif value>=int(1e4): return f"{round(value/int(1e4), 1)}만"
        else: return f"{round(value, 1)}"

    try: #누적 조회수 값 dailychannel에서 받아오도록 수정
        ad_query = f"""
                SELECT
                    COUNT(*) as ad_count,
                    MAX(v."videoPublishedAt") as last_update,
                    SUM(CAST(v."videoViewCount" AS INTEGER)) as total_views,
                    SUM(CAST(v."videoLikeCount" AS INTEGER)) as total_likes,
                    SUM(CAST(v."commentCount" AS INTEGER)) as total_comments
                FROM public."Video" v
                WHERE v."channel_id" = '{id_name_pair[channel_name]}'
                AND v."hasPaidProductPlacement" = true
            """

        df = pd.read_sql(ad_query, db_engine)

        ad_count = df.iloc[0]['ad_count']
        total_views = df.iloc[0]['total_views']
        total_likes = df.iloc[0]['total_likes']
        total_comments = df.iloc[0]['total_comments']

        avg_views = total_views / ad_count if ad_count > 0 else 0
        avg_likes = total_likes / ad_count if ad_count > 0 else 0
        avg_comments = total_comments / ad_count if ad_count > 0 else 0
    
    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return [{
        "광고 영상": f"{simplify(ad_count)}개",
        "누적 조회수": f"{simplify(total_views)}회 (영상 당 평균 {simplify(avg_views)}회)",
        "누적 좋아요": f"{simplify(total_likes)}개 (영상 당 평균 {simplify(avg_likes)}개)",
        "누적 댓글": f"{simplify(total_comments)}개 (영상 당 평균 {simplify(avg_comments)}개)"
    }]


@dashboard_router.get("/profitability/ad-vs-normal/{channel_name}")
async def compare_ad_vs_normal(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    광고 영상과 일반 영상의 성과 비교 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명 (나중에 채널 ID로 변경해야할 것 같음)
    Returns:
        [
            {"항목": "영상 수", "일반 영상": "368개", "광고 영상": "35개", "비교": "-"},
            {"항목": "업데이트 주기", "일반 영상": "월 4개", "광고 영상": "월 2개", "비교": "-"},
            {"항목": "평균 조회수", "일반 영상": "100,000회", "광고 영상": "20,000회", "비교": "-80,000"},
            {"항목": "평균 좋아요 비율", "일반 영상": "0.2%", "광고 영상": "0.001%", "비교": "-0.199%"},
            {"항목": "평균 댓글 비율", "일반 영상": "0.01%", "광고 영상": "0.005%", "비교": "-0.005%"}
        ]
    """
    channel_query = f"""
        SELECT 
            SUM(CASE WHEN "hasPaidProductPlacement" = true THEN 1 ELSE 0 END) AS adsViewCount,
        FROM public."Video"
        JOIN 
        WHERE "channel_id" = '{channel_id}'
        """
    try:
        df = pd.read_sql(channel_query, db_engine, params=(channel_name))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return [{
        "영상 수": {"일반 영상":..., "광고 영상":..., "비교":"-"},
         "업데이트 주기": {"일반 영상":..., "광고 영상":..., "비교":"-"},
         "평균 조회수": {"일반 영상":..., "광고 영상":..., "비교":...},
         "평균 좋아요 비율": {"일반 영상":..., "광고 영상":..., "비교":...},
         "평균 댓글 비율": {"일반 영상":..., "광고 영상":..., "비교":...}
         }]

# 광고 영상 성적
@dashboard_router.get("/profitability/ad-performance/{channel_name}")
async def get_ad_performance(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    성과가 좋은 영상, 썸네일을 알려줌
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        
    """
    
    try: #조회수 dailyChannel로 수정
        def simplify(value):
            if value >= int(1e8): 
                return f"{round(value/int(1e8), 1)}억"
            elif value >= int(1e4): 
                return f"{round(value/int(1e4), 1)}만"
            elif value >= int(1e3): 
                return f"{round(value/int(1e3), 1)}천"
            else: 
                return f"{round(value, 1)}"
                
        video_performance_query = f"""
            WITH video_metrics AS (
                SELECT 
                    "videoTitle",
                    "videoThumbnails",
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    ROUND((CAST("commentCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as comment_rate,
                    ROUND((CAST("videoLikeCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as like_rate,
                    ROUND(CAST("videoCTR" AS FLOAT)::numeric, 2) as ctr
                FROM public."Video"
                WHERE "channel_id" = '{id_name_pair[channel_name]}'
            )
            SELECT 
                "videoTitle" as "제목",
                "videoThumbnails" as "썸네일",
                view_count as "조회수",
                comment_rate as "댓글 참여율",
                like_rate as "좋아요 참여율",
                ctr as "노출 클릭률"
            FROM video_metrics
            ORDER BY view_count DESC
            LIMIT 3
        """
        
        thumbnail_performance_query = f"""
            WITH thumbnail_metrics AS (
                SELECT 
                    "videoTitle",
                    "videoThumbnails",
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    ROUND((CAST("commentCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as comment_rate,
                    ROUND((CAST("videoLikeCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as like_rate,
                    ROUND(CAST("videoCTR" AS FLOAT)::numeric, 2) as ctr
                FROM public."Video"
                WHERE "channel_id" = '{id_name_pair[channel_name]}'
            )
            SELECT 
                "videoTitle" as "제목",
                "videoThumbnails" as "썸네일",
                view_count as "조회수",
                comment_rate as "댓글 참여율",
                like_rate as "좋아요 참여율",
                ctr as "노출 클릭률"
            FROM thumbnail_metrics
            ORDER BY ctr DESC
            LIMIT 3
        """
        top_videos_df = pd.read_sql(video_performance_query, db_engine)
        top_thumbnails_df = pd.read_sql(thumbnail_performance_query, db_engine)

        for df in [top_videos_df, top_thumbnails_df]:
            df["조회수"] = df["조회수"].apply(lambda x: simplify(x))
            df.insert(3, "평균 조회율", "4.5%") #수정
            df["댓글 참여율"] = df["댓글 참여율"].apply(lambda x: f"{x}%")
            df["좋아요 참여율"] = df["좋아요 참여율"].apply(lambda x: f"{x}%")
            df["노출 클릭률"] = df["노출 클릭률"].apply(lambda x: f"{x}%")
            df = df[["제목", "썸네일", "조회수", "평균 조회율", "댓글 참여율", "좋아요 참여율", "노출 클릭률"]]

        result = {
            "많은 사랑을 받은 영상": top_videos_df.to_dict(orient='records'),
            "많은 사랑을 받은 썸네일": top_thumbnails_df.to_dict(orient='records')
        }
        
        return result

    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


###################
## 시청자 관계 API ##
###################
@dashboard_router.get("/audience/engagement/{channel_name}")
async def get_audience_engagement(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    시청자의 채널 참여도 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        [
            {"좋아요 비율": "0.11%"},
            {"댓글 비율": "3.69%"},
            {"공유 비율": "5.87%"}
        ]
    """

    try:
        engagement_query = f"""
            SELECT 
                SUM(CAST(v."videoViewCount" AS INTEGER)) as total_views,
                SUM(CAST(v."videoLikeCount" AS INTEGER)) as total_likes,
                SUM(CAST(v."commentCount" AS INTEGER)) as total_comments,
                SUM(CAST(v."videoShareCount" AS INTEGER)) as total_shares
            FROM public."Video" v
            WHERE v."channel_id" = '{id_name_pair[channel_name]}'
        """
        df = pd.read_sql(engagement_query, db_engine)
        
        total_views = df.iloc[0]['total_views'] #수정정
        total_likes = df.iloc[0]['total_likes']
        total_comments = df.iloc[0]['total_comments']
        total_shares = df.iloc[0]['total_shares']
        
        like_ratio = (total_likes / total_views * 100) if total_views > 0 else 0
        comment_ratio = (total_comments / total_views * 100) if total_views > 0 else 0
        share_ratio = (total_shares / total_views * 100) if total_views > 0 else 0
    
    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return [
        {"좋아요 비율": f"{like_ratio:.2f}%"},
        {"댓글 비율": f"{comment_ratio:.2f}%"},
        {"공유 비율": f"{share_ratio:.2f}%"}
    ]

@dashboard_router.get("/audience/creator-communication/{channel_name}")
async def get_creator_communication(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    크리에이터가 시청자와 소통하는 하는 정도를 나타내는 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        [
            {"라이브 수": 12},
            {"경쟁 채널 라이브 수": 5}, -> 경쟁 채널 : 비슷한 규모(구독자 수)의 채널들
            {"라이브 평균 시청자 수": "3151"명},
            {"대댓글 수": 300},-> replies에서 channel displyname과 일치하는 작성자 아이디가 있는 댓글 count
            {"경쟁 채널 평균 대댓글 수": 120}
        ]
    """
    try:
        #채널의 구독자 수 범위 파악용
        channel_info_query = f"""
            SELECT "subscriberCount", "DisplayName"
            FROM public."Channel"
            WHERE "id" = '{id_name_pair[channel_name]}'
        """
        channel_info = pd.read_sql(channel_info_query, db_engine)
        subscriber_count = channel_info.iloc[0]['subscriberCount']
        display_name = channel_info.iloc[0]['DisplayName']  # 현재 채널 아이디 (대댓글 확인용)

        # # PostgreSQL에서 특수문자 처리
        # sescaped_display_name = display_name.replace("'", "''").replace('@', '\\@')
        
        # 현재 채널의 라이브 수
        live_query = f"""
            SELECT "LiveBroadcastingCount",
                "LiveBroadcastingViewer"
            FROM public."Channel"
            WHERE "id" = '{id_name_pair[channel_name]}'
        """
        
        # 경쟁 채널들의 라이브 수
        competitor_live_query = f"""
            SELECT COALESCE(AVG("LiveBroadcastingCount"), 0) as avg_competitor_live
            FROM public."Channel"
            WHERE CAST("subscriberCount" AS FLOAT) BETWEEN CAST({subscriber_count} AS FLOAT) * 0.5 AND CAST({subscriber_count} AS FLOAT) * 1.5
            AND "id" != '{id_name_pair[channel_name]}'
        """
        
        # 대댓글 수 계산
        search_term = f'@{display_name}'
        replies_query = f"""
            SELECT COUNT(*) as reply_count
            FROM public."Comments"
            WHERE strpos(replies, '@{display_name}') > 0
        """
        
        # # 경쟁 채널들의 평균 대댓글 수
        competitor_replies_query = f"""
            SELECT COALESCE(AVG(reply_count), 0) as avg_competitor_replies
            FROM (
                SELECT 
                    ch."id",
                    COUNT(*) as reply_count
                FROM public."Channel" ch
                JOIN public."Comments" cm ON strpos(cm."replies", '@' || ch."DisplayName") > 0
                WHERE CAST(ch."subscriberCount" AS FLOAT) BETWEEN CAST({subscriber_count} AS FLOAT) * 0.5 AND CAST({subscriber_count} AS FLOAT) * 1.5
                AND ch."id" != '{id_name_pair[channel_name]}'
                GROUP BY ch."id"
            ) subquery
        """

        # 최종 메트릭릭
        live_data = pd.read_sql(live_query, db_engine).to_dict('records')[0]
        competitor_live = pd.read_sql(competitor_live_query, db_engine).to_dict('records')[0]
        replies_data = pd.read_sql(replies_query, db_engine).to_dict('records')[0]
        competitor_replies = pd.read_sql(competitor_replies_query, db_engine).to_dict('records')[0]
        
        return [
            {"라이브 수": int(live_data['LiveBroadcastingCount'])},
            {"경쟁 채널 라이브 수": int(competitor_live['avg_competitor_live'])},
            {"라이브 평균 시청자 수": int(live_data['LiveBroadcastingViewer'])},
            {"대댓글 수": int(replies_data['reply_count'])},
            {"경쟁 채널 평균 대댓글 수": int(competitor_replies['avg_competitor_replies'])}
        ]

    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@dashboard_router.get("/audience/targeting-strategy/{channel_name}")
async def get_targeting_strategy(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    시청자 타겟팅 전략 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        [
            {"타겟 시청자 특성": "남성", "10~20대"}, <- 수정
            {"키워드": "178만"명}, <- Video-tag, description 해시태그 각 키워드 개수 센 후 랭킹, 상위 n개 뽑기
            {"영상 업로드 시간": 12, 1}, <- 다시 수정
            {"영상 시청 시간": 12, 1}, <- 다시 수정
            {"일반/광고 영상 비율" : 0.3} <- 광고영상이 전체의 30%
        ]
    """
    try:
        video_query = f"""
            SELECT 
                v.tags,
                v."videoDescription"
            FROM public."Video" v
            WHERE v."channel_id" = '{id_name_pair[channel_name]}'
        """
        video_df = pd.read_sql(video_query, db_engine)
        
        all_keywords = []
        for tags in video_df['tags']:
            if tags:
                all_keywords.extend([tag.strip('#').strip('{}').lower().replace('"', '').replace('\\', '').replace('\n', '') for tag in tags.split(',')])
        for description in video_df['videoDescription']:
            if description:
                all_keywords.extend([word.strip('#').lower().replace('"', '').replace('\\', '').replace('\n', '') for word in description.split('#') if word.strip()])
        
        # 키워드 빈도
        keyword_counts = Counter(all_keywords)
        top_keywords = dict(keyword_counts.most_common())
        
        # 영상 업로드 시간 분석
        upload_time_query = f"""
            SELECT 
                SUBSTRING(v."videoPublishedAt", 12, 2) AS upload_hour
            FROM public."Video" v
            WHERE v."channel_id" = '{id_name_pair[channel_name]}'
            GROUP BY upload_hour
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """
        upload_time_df = pd.read_sql(upload_time_query, db_engine)
        upload_time_list = [int(upload_time_df.iloc[0]['upload_hour']), int(upload_time_df.iloc[0]['upload_hour']) + 1]

        view_time_query = f"""
            SELECT 
                SUBSTRING(c."commentPublishedAt", 12, 2) AS view_hour,
                COUNT(*) AS comment_count
            FROM public."Comments" c
            JOIN public."Video" v ON c."vId" = v."vId"
            WHERE v."channel_id" = '{id_name_pair[channel_name]}'
            GROUP BY view_hour
            ORDER BY comment_count DESC
            LIMIT 1
        """
        view_time_df = pd.read_sql(view_time_query, db_engine)
        view_time_list = [int(view_time_df.iloc[0]['view_hour']), int(view_time_df.iloc[0]['view_hour']) + 1]

        # 일반/광고 영상 비율
        ad_video_query = f"""
            SELECT 
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN 1 ELSE 0 END) AS ad_count,
                COUNT(*) AS total_count
            FROM public."Video"
            WHERE "channel_id" = '{id_name_pair[channel_name]}'
        """
        ad_video_df = pd.read_sql(ad_video_query, db_engine)
        ad_ratio = ad_video_df.iloc[0]['ad_count'] / ad_video_df.iloc[0]['total_count']
        
        return [
            {"타겟 시청자 특성": "남성, 10-20대"},
            {"키워드": ", ".join([k for k, v in list(top_keywords.items())[5:11]if len(k) < 15])},
            {"영상 업로드 시간": upload_time_list},
            {"영상 시청 시간": view_time_list},
            {"일반/광고 영상 비율": f"{ad_ratio:.2%}"}
        ]
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

###################
## 채널 성과 API ##
###################

# 채널 배너
@dashboard_router.get("/performance/channel-banner/{channel_name}")
async def get_channel_banner(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    채널 기본 정보 데이터 반환환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        [
            {"채널 이름": "피식대학"},
            {"구독자": "178만"명}, #수정, dailyChannel 최근 값으러러
            {"동영상": "1.2천"개}
        ]
    """
    try:
        channel_query = f"""
        SELECT 
            "title",
            CAST("subscriberCount" AS INTEGER) AS "subscriberCount", 
            CAST("videoCount" AS INTEGER) AS "videoCount"
        FROM public."Channel"
        WHERE "id" = '{id_name_pair[channel_name]}'
        """
        
        channel_info = pd.read_sql(channel_query, db_engine)
        
        def simplify(value):
            if value>=int(1e8): return f"{round(value/int(1e8), 1)}억"
            elif value >= int(1e4): return f"{round(value/int(1e4), 1)}만"
            elif value >= int(1e3): return f"{round(value/int(1e3), 1)}천"
            else: return f"{int(value)}"
        
        return [
            {"채널 이름": channel_info.iloc[0]['title']},
            {"구독자": simplify(channel_info.iloc[0]['subscriberCount']) + "명"},
            {"동영상": simplify(channel_info.iloc[0]['videoCount']) + "개"}
        ]

    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 많이 사랑 받는 영상 / 많이 사랑 받는 썸네일
@dashboard_router.get("/performance/channel-performance/{channel_name}")
async def get_channel_performance(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    성과가 좋은 영상, 썸네일을 알려줌
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        
    """
    
    try: #조회수 dailyChannel로 수정
        def simplify(value):
            if value >= int(1e8): 
                return f"{round(value/int(1e8), 1)}억"
            elif value >= int(1e4): 
                return f"{round(value/int(1e4), 1)}만"
            elif value >= int(1e3): 
                return f"{round(value/int(1e3), 1)}천"
            else: 
                return f"{round(value, 1)}"
                
        video_performance_query = f"""
            WITH video_metrics AS (
                SELECT 
                    "videoTitle",
                    "videoThumbnails",
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    ROUND((CAST("commentCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as comment_rate,
                    ROUND((CAST("videoLikeCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as like_rate,
                    ROUND(CAST("videoCTR" AS FLOAT)::numeric, 2) as ctr
                FROM public."Video"
                WHERE "channel_id" = '{id_name_pair[channel_name]}'
            )
            SELECT 
                "videoTitle" as "제목",
                "videoThumbnails" as "썸네일",
                view_count as "조회수",
                comment_rate as "댓글 참여율",
                like_rate as "좋아요 참여율",
                ctr as "노출 클릭률"
            FROM video_metrics
            ORDER BY view_count DESC
            LIMIT 3
        """
        
        thumbnail_performance_query = f"""
            WITH thumbnail_metrics AS (
                SELECT 
                    "videoTitle",
                    "videoThumbnails",
                    CAST("videoViewCount" AS FLOAT) as view_count,
                    ROUND((CAST("commentCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as comment_rate,
                    ROUND((CAST("videoLikeCount" AS FLOAT) / CAST("videoViewCount" AS FLOAT) * 100)::numeric, 2) as like_rate,
                    ROUND(CAST("videoCTR" AS FLOAT)::numeric, 2) as ctr
                FROM public."Video"
                WHERE "channel_id" = '{id_name_pair[channel_name]}'
            )
            SELECT 
                "videoTitle" as "제목",
                "videoThumbnails" as "썸네일",
                view_count as "조회수",
                comment_rate as "댓글 참여율",
                like_rate as "좋아요 참여율",
                ctr as "노출 클릭률"
            FROM thumbnail_metrics
            ORDER BY ctr DESC
            LIMIT 3
        """
        top_videos_df = pd.read_sql(video_performance_query, db_engine)
        top_thumbnails_df = pd.read_sql(thumbnail_performance_query, db_engine)

        for df in [top_videos_df, top_thumbnails_df]:
            df["조회수"] = df["조회수"].apply(lambda x: simplify(x))
            df.insert(3, "평균 조회율", "4.5%") #수정
            df["댓글 참여율"] = df["댓글 참여율"].apply(lambda x: f"{x}%")
            df["좋아요 참여율"] = df["좋아요 참여율"].apply(lambda x: f"{x}%")
            df["노출 클릭률"] = df["노출 클릭률"].apply(lambda x: f"{x}%")
            df = df[["제목", "썸네일", "조회수", "평균 조회율", "댓글 참여율", "좋아요 참여율", "노출 클릭률"]]

        result = {
            "많은 사랑을 받은 영상": top_videos_df.to_dict(orient='records'),
            "많은 사랑을 받은 썸네일": top_thumbnails_df.to_dict(orient='records')
        }
        
        return result

    except KeyError:
        raise HTTPException(status_code=404, detail="Channel not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# 채널 평균 조회수
@dashboard_router.get("/performance/channel-viewcount/{channel_name}")
async def get_channel_viewcount(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    method 설명
    Parameters:
        
    Returns:
        
    """
    channel_query = f"""
        SELECT 
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoViewCount" AS FLOAT) ELSE 0 END) AS adsviewcount,
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoLikeCount" AS FLOAT) ELSE 0 END) AS adslikecount
        FROM public."Video"
        JOIN 
        WHERE "channel_id" = '{channel_id}'
        """
    try:
        df = pd.read_sql(channel_query, db_engine, params=(channel_name))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    return

# 채널 성장 추세
@dashboard_router.get("/performance/channel-growth/{channel_name}")
async def get_channel_growth(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    method 설명
    Parameters:
        
    Returns:
        
    """
    channel_query = f"""
        SELECT 
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoViewCount" AS FLOAT) ELSE 0 END) AS adsviewcount,
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoLikeCount" AS FLOAT) ELSE 0 END) AS adslikecount
        FROM public."Video"
        JOIN 
        WHERE "channel_id" = '{channel_id}'
        """
    try:
        df = pd.read_sql(channel_query, db_engine, params=(channel_name))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    return

# 채널 특징
@dashboard_router.get("/performance/channel-feature/{channel_name}")
async def get_channel_feature(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    method 설명
    Parameters:
        
    Returns:
        
    """
    channel_query = f"""
        SELECT 
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoViewCount" AS FLOAT) ELSE 0 END) AS adsviewcount,
                SUM(CASE WHEN "hasPaidProductPlacement" = true THEN CAST("videoLikeCount" AS FLOAT) ELSE 0 END) AS adslikecount
        FROM public."Video"
        JOIN 
        WHERE "channel_id" = '{channel_id}'
        """
    try:
        df = pd.read_sql(channel_query, db_engine, params=(channel_name))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    return