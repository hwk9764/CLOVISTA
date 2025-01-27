from fastapi import APIRouter, HTTPException, Depends, Request
import pandas as pd
import psycopg2

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
        SELECT "id", "title"
        FROM "Channel";
        """
with conn.cursor() as cur:
    id_df = pd.read_sql(query, conn)
    name_to_id = {name:int(id) for name, id in zip(id_df['title'].values, id_df['id'].values)}

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
        [{
        "조회수_유저": 1,115,132,
        "조회수_평균": 1,000,000,
        #"후원_유저": 568,186,
        #"후원_평균": 123,456
        }]
    """

    # 코드 테스트할 때는 try, except 빼는 것을 추천
    try:
        channel_query = f"""
        SELECT "viewCount", "Donation",
            (SELECT AVG(CAST("viewCount" as float)) FROM "Channel") as avg_viewcount,
            (SELECT AVG(CAST("Donation" as float)) FROM "Channel") as avg_donation
        FROM public."Channel"
        WHERE "id" = '{name_to_id[channel_name]}'
        """
        df = pd.read_sql(channel_query, db_engine)
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        # 전처리 코드 추가
        viewcount = int(df.iloc[0]['viewCount'])
        avg_viewcount = int(df.iloc[0]['avg_viewcount'])
        view_profit_user = (viewcount*2, int(viewcount*4.5))
        view_profit_avg = (avg_viewcount*2, int(avg_viewcount*4.5))
        #donation_profit_user = int(df.iloc[0]['Donation'])
        #donation_profit_avg = int(df.iloc[0]['avg_donation'])

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
    query = """
        SELECT
            COUNT(*) as ad_count,
            MAX("videoPublishedAt") as last_update,
            SUM(CAST("videoViewCount" AS INTEGER)) as total_views,
            SUM(CAST("videoLikeCount" AS INTEGER)) as total_likes,
            SUM(CAST("commentCount" AS INTEGER)) as total_comments
        FROM public."Video" v
        JOIN public."Channel" c ON v.channel_id = c.id
        WHERE c."name" = %s AND "hasPaidProductPlacement" = true
    """
    try:
        df = pd.read_sql(query, db_engine, params=(channel_name,))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        ad_count = df.iloc[0]['ad_count']
        total_views = df.iloc[0]['total_views']
        total_likes = df.iloc[0]['total_likes']
        total_comments = df.iloc[0]['total_comments']
        avg_views = total_views / ad_count
        avg_likes = total_likes / ad_count
        avg_comments = total_comments / ad_count
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return [{
        "광고 영상": f"{simplify(ad_count)}개)",
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
        [{
        "영상 수": {"일반 영상":"368개", "광고 영상":"35개", "비교":"-"},
         "업데이트 주기": {"일반 영상":"월 4개", "광고 영상":"월 2개", "비교":"-"},
         "평균 조회수": {"일반 영상":"100,000회", "광고 영상":"20,000회", "비교":"-80,000"},
         "평균 좋아요 비율": {"일반 영상":"0.2%", "광고 영상":"0.001%", "비교":"-0.199%"},
         "평균 댓글 비율": {"일반 영상":"0.01%", "광고 영상":"0.005%", "비교":"-0.005%"}
         }]
    """
    noads_query = f"""
        SELECT
                SUM(CAST(v."videoViewCount" AS FLOAT)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS viewcount,
                SUM(CAST(v."videoLikeCount" AS FLOAT)/NULLIF(CAST(v."videoViewCount" AS FLOAT), 0)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS likecount,
                SUM(CAST(v."commentCount" AS FLOAT)/NULLIF(CAST(v."videoViewCount" AS FLOAT), 0)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS commentcount,
                COUNT(*) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS videocount
        FROM public."Video" v
        LEFT JOIN public."Channel" c
        ON v."channel_id" = c."id"
        WHERE v."channel_id" = '{name_to_id[channel_name]}' AND v."hasPaidProductPlacement" = false
        """
    ads_query = f"""
        SELECT
                SUM(CAST(v."videoViewCount" AS FLOAT)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS viewcount,
                SUM(CAST(v."videoLikeCount" AS FLOAT)/NULLIF(CAST(v."videoViewCount" AS FLOAT), 0)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS likecount,
                SUM(CAST(v."commentCount" AS FLOAT)/NULLIF(CAST(v."videoViewCount" AS FLOAT), 0)) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS commentcount,
                COUNT(*) FILTER (WHERE TO_TIMESTAMP("videoPublishedAt", 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '90 days') AS videocount
        FROM public."Video" v
        LEFT JOIN public."Channel" c
        ON v."channel_id" = c."id"
        WHERE v."channel_id" = '{name_to_id[channel_name]}' AND v."hasPaidProductPlacement" = true
        """
    try:
        noads_df = pd.read_sql(noads_query, db_engine)
        ads_df = pd.read_sql(ads_query, db_engine)
        if noads_df.empty or ads_df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        
        # 영상 수
        video_count = int(noads_df.iloc[0]['videocount']) if noads_df.iloc[0]['videocount'] != None else 0
        ads_video_count = int(ads_df.iloc[0]['videocount']) if ads_df.iloc[0]['videocount'] != None else 0
        # 업데이트 주기
        period = round(video_count/3, 1)
        ads_period = round(ads_video_count/3, 1)
        # 평균 조회수
        view_count = int(noads_df.iloc[0]['viewcount'])//video_count if video_count != 0 else 0   # 전체 조회수
        ads_view_count = int(ads_df.iloc[0]['viewcount'])//ads_video_count if ads_video_count != 0 else 0   # 광고 영상 조회수   
        # 평균 좋아요 비율
        like_ratio = noads_df.iloc[0]['likecount']/video_count*100 if video_count !=0 else 0    # 전체 좋아요 합산
        ads_like_ratio = ads_df.iloc[0]['likecount']/ads_video_count*100 if ads_video_count != 0 else 0    # 광고 영상 좋아요 합산
        # 평균 댓글 비율
        comment_ratio = noads_df.iloc[0]['commentcount']/video_count*100 if video_count !=0 else 0 # 전체 댓글 합산
        ads_comment_ratio = ads_df.iloc[0]['commentcount']/ads_video_count*100 if ads_video_count != 0 else 0 # 광고 영상 좋아요 합산산
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return [{
        "영상 수": {"일반 영상":f"{video_count:,}개", "광고 영상":f"{ads_video_count:,}개", "비교":"-"},
         "업데이트 주기": {"일반 영상":f"월 {period}개", "광고 영상":f"월 {ads_period}개", "비교":"-"},
         "평균 조회수": {"일반 영상":f"{view_count:,}", "광고 영상":f"{ads_view_count:,}", "비교":f"{view_count-ads_view_count:,}"},
         "평균 좋아요 비율": {"일반 영상":f"{round(like_ratio,2)}%", "광고 영상":f"{round(ads_like_ratio,2)}%", "비교":f"{round(like_ratio-ads_like_ratio, 2)}%"},
         "평균 댓글 비율": {"일반 영상":f"{round(comment_ratio,2)}%", "광고 영상":f"{round(ads_comment_ratio,2)}%", "비교":f"{round(comment_ratio-ads_comment_ratio,2)}%"}
         }]

# 광고 영상 성적
@dashboard_router.get("profitability/ad-performance/{channel_name}")
async def get_ads_performance(channel_name: str, db_engine=Depends(get_db_engine)):
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
            {"공유 비율": "5.87%"} --> 데이터가 없어서 일단 지움
        ]
    """
    query = """
        SELECT 
            c.name,
            SUM(CAST(v."videoViewCount" AS INTEGER)) as total_views,
            SUM(CAST(v."videoLikeCount" AS INTEGER)) as total_likes,
            SUM(CAST(v."commentCount" AS INTEGER)) as total_comments
        FROM public."Channel" c
        JOIN public."Video" v ON c.id = v.channel_id
        WHERE c.name = %s
        GROUP BY c.name
    """
    try:
        df = pd.read_sql(query, db_engine, params=(channel_name,))
        if df.empty:
            raise HTTPException(status_code=404, detail="Channel not found.")
        
        total_views = df.iloc[0]['total_views']
        total_likes = df.iloc[0]['total_likes']
        total_comments = df.iloc[0]['total_comments']
        
        like_ratio = (total_likes / total_views * 100) if total_views > 0 else 0
        comment_ratio = (total_comments / total_views * 100) if total_views > 0 else 0
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    return [
        {"좋아요 비율": f"{like_ratio:.2f}%"},
        {"댓글 비율": f"{comment_ratio:.2f}%"}
    ]

@dashboard_router.get("/audience/creator-communication/{channel_name}")
async def get_creator_communication(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    크리에이터가 시청자와 소통하는 하는 정도를 나타내는 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        어떻게 전달할지 논의 필요. 프론트에 값만 전달할지...?
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
    return None


@dashboard_router.get("/audience/targeting-strategy/{channel_name}")
async def get_targeting_strategy(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    시청자 타겟팅 전략 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명
    Returns:
        어떻게 전달할지 논의 필요
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
    return None


###################
## 채널 성과 API ##
###################

# 채널 배너
@dashboard_router.get("performance/channel-banner/{channel_name}")
async def get_channel_banner(channel_name: str, db_engine=Depends(get_db_engine)):
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

# 많이 사랑 받는 영상 / 많이 사랑 받는 썸네일
@dashboard_router.get("performance/channel-performance/{channel_name}")
async def get_channel_performance(channel_name: str, db_engine=Depends(get_db_engine)):
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

# 채널 평균 조회수
@dashboard_router.get("performance/channel-viewcount/{channel_name}")
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
@dashboard_router.get("performance/channel-growth/{channel_name}")
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
@dashboard_router.get("performance/channel-feature/{channel_name}")
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