from fastapi import APIRouter, HTTPException, Depends, Request
import pandas as pd

dashboard_router = APIRouter()


def get_db_engine(request: Request):
    """
    FastAPI의 상태 객체에서 DB 엔진을 가져옵니다.
    """
    return request.app.state.db_engine


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
            {"date": "2024-01-01", "value": 10},
            {"date": "2024-01-02", "value": 15},
            {"date": "2024-01-03", "value": 20}
        ]
    """
    # 관련 데이터 가져오기
    # 날짜별 아니고 {내 조회수 수익:, 평균 조회수 수익:, 내 슈퍼챗 수익:, 평균 슈퍼챗 수익:} 으로 보내기
    
    # 코드 테스트할 때는 try, except 빼는 것을 추천
    try:
        channel_query = f'SELECT * FROM public."Channel" WHERE channel_name = {channel_name}'
        channel_df = pd.read_sql(channel_query, db_engine, params=[channel_name])
        if not channel_df:
            raise HTTPException(status_code=404, detail="Channel not found.")
        # 전처리 코드 추가

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


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
        else: f"{round(value, 1)}"
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

    df = pd.read_sql(query, db_engine, params=(channel_name,))

    ad_count = df.iloc[0]['ad_count']
    total_views = df.iloc[0]['total_views']
    total_likes = df.iloc[0]['total_likes']
    total_comments = df.iloc[0]['total_comments']
    avg_views = total_views / ad_count
    avg_likes = total_likes / ad_count
    avg_comments = total_comments / ad_count

    return [{
        "광고 영상": f"{ad_count}개",
        "누적 재생": f"{simplify(total_views)}회 (영상 당 평균 {simplify(avg_views)}회)",
        "누적 좋아요": f"{simplify(total_likes)}개 (영상 당 평균 {simplify(avg_likes)}개)",
        "누적 댓글": f"{simplify(total_comments)}개 (영상 당 평균 {int(avg_comments)}개)"
    }]


@dashboard_router.get("/profitability/ad-vs-normal/{channel_name}")
async def compare_ad_vs_normal(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    광고 영상과 일반 영상의 성과 비교 데이터를 반환
    Parameters:
        channel_name: 유튜브 채널명 (나중에 채널 ID로 변경해야할 것 같음)
    Returns:
        [
            {"항목": "동영상", "일반 영상": "368개", "광고 영상": "35개", "비교": "-"},
            {"항목": "업데이트 주기", "일반 영상": "4개/월", "광고 영상": "2개/월", "비교": "-"},
            ...

        ]
    """
    return [
        {"항목": "동영상", "일반 영상": "368개", "광고 영상": "35개", "비교": "-"},
        {"항목": "업데이트 주기", "일반 영상": "4개/월", "광고 영상": "2개/월", "비교": "-"},
    ]


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
    
    df = pd.read_sql(query, db_engine, params=(channel_name,))
    
    total_views = df.iloc[0]['total_views']
    total_likes = df.iloc[0]['total_likes']
    total_comments = df.iloc[0]['total_comments']
    
    like_ratio = (total_likes / total_views * 100) if total_views > 0 else 0
    comment_ratio = (total_comments / total_views * 100) if total_views > 0 else 0
    
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
        어떻게 전달할지 논의 필요
    """
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
    return None


###################
## 채널 성과 API ##
###################
