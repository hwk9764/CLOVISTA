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
    조회수 수입 및 후원 수입 데이터를 반환
    Parameters:
        Channel_name: 유튜브 채널명 (나중에 채널 ID로 변경해야할 것 같음)
    Returns:
        [
            {"date": "2024-01-01", "value": 10},
            {"date": "2024-01-02", "value": 15},
            {"date": "2024-01-03", "value": 20}
        ]
    """
    # 코드 테스트할 때는 try, except 빼는 것을 추천
    try:
        query = f'SELECT * FROM public."Channel" WHERE channel_name = %s'
        channel_df = pd.read_sql(query, db_engine, params=[channel_name])
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
    return [
        {
            "광고영상": "35개 (8달 전 업데이트)",
            "누적 재생": "1.2천만 (영상당 평균 ~~)",
            "누적 좋아요": "33.8만 (영상당 평균 ~~)",
            "누적 댓글": "7천만 (영상당 평균 ~~~)",
        }
    ]


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
            {"공유 비율": "5.87*"}
        ]
    """
    return [{"좋아요 비율": "0.11%"}, {"댓글 비율": "3.69%"}, {"공유 비율": "5.87*"}]


@dashboard_router.get("/audience/creator-communication/{channel_name}")
async def get_creator_communication(channel_name: str, db_engine=Depends(get_db_engine)):
    """
    채널주 소통의 정도 데이터를 반환
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
