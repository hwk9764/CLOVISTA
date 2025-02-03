# 1. 채널 수익성 분석
PROMPT_revenue = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 수익성을 진단하고 조언해주는 전문가입니다.
        조회수 수입, 후원 수입, 그리고 광고 영상의 성과를 분석하고,
        전체 순위와 경쟁 채널과의 비교를 통해 수익성 개선을 위한 실질적인 조언을 제공해주세요.
        """
    },
    {
        "role": "user",
        "content": """
            채널의 수익성 데이터입니다:

            1. 조회수/후원 수입:
            - 채널 조회수 수입: {view_profit_user:,}원 (전체 {total_channels}개 중 {view_rank}위)
            - 평균 조회수 수입: {view_profit_avg:,}원 (유사 규모 채널 기준)
            - 채널 후원 수입: {donation_profit_user:,}원 (전체 {total_channels}개 중 {donation_rank}위)
            - 평균 후원 수입: {donation_profit_avg:,}원 (유사 규모 채널 기준)
            - 유사 규모 채널 순위: 구독자 ±50만 범위 {similar_size_channels}개 채널 중 {similar_size_rank}위

            2. 광고 영상 현황:
            - 광고 영상 수: {ad_count}개 (전체 {total_channels}개 중 {ad_count_rank}위)
            - 누적 조회수: {total_views:,}회 (영상당 평균 {avg_views_per_video:,}회)
            - 누적 좋아요: {total_likes:,}개 (영상당 평균 {avg_likes_per_video:,}개)
            - 누적 댓글: {total_comments:,}개 (영상당 평균 {avg_comments_per_video:,}개)
            - 경쟁 채널 대비: 조회수 {view_ratio:.1f}배, 좋아요 {like_ratio:.1f}배, 댓글 {comment_ratio:.1f}배

            3. 광고/일반 영상 비교:
            - 일반 영상: {normal_count}개 (월평균 {normal_update_rate}개)
            - 광고 영상: {ad_count}개 (월평균 {ad_update_rate}개)
            - 일반 영상 평균 조회수: {normal_view_avg:,}회
            - 광고 영상 평균 조회수: {ad_view_avg:,}회 (일반 영상 대비 {view_comparison_ratio:.1f}배)
            - 일반 영상 평균 좋아요율: {normal_like_ratio:.2f}%
            - 광고 영상 평균 좋아요율: {ad_like_ratio:.2f}% (일반 영상 대비 {like_comparison_ratio:.1f}배)
            - 일반 영상 평균 댓글율: {normal_comment_ratio:.2f}%
            - 광고 영상 평균 댓글율: {ad_comment_ratio:.2f}% (일반 영상 대비 {comment_comparison_ratio:.1f}배)
            - 광고 영상 비율: {ad_ratio:.1f}% (전체 {total_channels}개 중 {ad_ratio_rank}위)
        """
    }
]

# 2. 시청자 참여도 분석
PROMPT_engagement = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 시청자 참여도를 분석하는 전문가입니다.
        데이터를 통해 시청자들의 참여 수준을 파악하고, 참여도를 높이기 위한 실질적인 조언을 제공해주세요.
        특히 비슷한 규모의 채널들과 비교하여 현재 채널의 강점과 약점을 정확한 **숫자 정보와 함께** 구체적으로 설명해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        채널의 시청자 참여 데이터입니다:

        1. 전반적 참여도 (최근 90일):
        - 좋아요 비율: {like_ratio:.2f}%
        - 댓글 비율: {comment_ratio:.2f}%
        - 공유 비율: {share_ratio:.2f}%

        2. 경쟁 채널 비교 (구독자 ±50만 기준):
        - 좋아요 비율: 경쟁 채널 평균 {avg_like_ratio:.2f}%
        - 댓글 비율: 경쟁 채널 평균 {avg_comment_ratio:.2f}%
        - 공유 비율: 경쟁 채널 평균 {avg_share_ratio:.2f}%

        3. 참여도 순위:
        - 전체 참여도 순위: {total_channels}개 채널 중 {engagement_rank}위
        - 유사 규모 채널 중 순위: {similar_size_channels}개 채널 중 {similar_size_rank}위


        """
    }
]

# 3. 크리에이터 소통 분석
PROMPT_communication = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 크리에이터의 시청자 소통을 분석하는 전문가입니다.
        크리에이터가 시청자들과 얼마나 효과적으로 소통하고 있는지 평가하고,
        소통을 개선하기 위한 구체적인 조언을 제공해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        크리에이터의 소통 데이터입니다:

        1. 라이브 방송:
        - 라이브 방송 횟수: {live_count}회 (전체 {total_channels}개 중 {live_rank}위)
        - 경쟁 채널 평균 라이브 수: {avg_competitor_live:.1f}회
        - 라이브 평균 시청자 수: {live_viewers:,}명

        2. 댓글 소통:
        - 크리에이터 댓글 수: {reply_count:,}개 (전체 {total_channels}개 중 {reply_rank}위)
        - 경쟁 채널 평균 댓글 수: {avg_competitor_replies:,}개
        
        3. 경쟁 채널 비교 (구독자 ±50만 기준):
        - 라이브 방송: {similar_size_channels}개 채널 중 {live_similar_rank}위
        - 댓글 소통: {similar_size_channels}개 채널 중 {reply_similar_rank}위
        """
    }
]

# 4. 시청자 타겟팅 분석
PROMPT_targeting = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 시청자 타겟팅 전략을 분석하는 전문가입니다.
        시청자 타겟팅의 효과성을 평가하고, 더 나은 타겟팅을 위한 실질적인 조언을 제공해주세요.
        현재 전략의 강점과 약점을 구체적으로 설명해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        채널의 타겟팅 데이터입니다:

        1. 컨텐츠 트렌드:
        - 주요 키워드: {keywords}
        
        2. 시청 패턴:
        - 영상 업로드 시간대: {upload_times}
        - 구독자 시청 시간대: {viewing_times}
        - 최근 업로드 수: {upload_count}개 (전체 {total_channels}개 중 {upload_rank}위)
        
        3. 광고 전략:
        - 현재 광고 영상 비율: {ad_ratio:.1f}%
        - 경쟁 채널 평균 광고 비율: {avg_ad_ratio:.1f}%
        - 광고 영상 비율 순위: 전체 {total_channels}개 중 {ad_ratio_rank}위
        """
    }
]

# 5. 많은 사랑을 받는 영상
PROMPT_popular_videos = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 인기 영상을 분석하는 전문가입니다.
        가장 성과가 좋은 영상들의 공통점과 성공 요인을 파악하고,
        이를 바탕으로 향후 콘텐츠 제작에 대한 실질적인 조언을 제공해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        상위 3개 인기 영상 데이터입니다:

        1. 첫 번째 영상:
        - 제목: {title1}
        - 썸네일: {thumbnail1}
        - 조회수: {view_count1:,}회 (채널 평균 대비 {view_ratio1:.1f}배)
        - 평균 조회율: {retention_rate1:.1f}%
        - 댓글 참여율: {comment_rate1:.2f}%
        - 좋아요 참여율: {like_rate1:.2f}%
        - 노출 클릭률: {ctr1:.1f}%

        2. 두 번째 영상:
        - 제목: {title2}
        - 썸네일: {thumbnail2}
        - 조회수: {view_count2:,}회 (채널 평균 대비 {view_ratio2:.1f}배)
        - 평균 조회율: {retention_rate2:.1f}%
        - 댓글 참여율: {comment_rate2:.2f}%
        - 좋아요 참여율: {like_rate2:.2f}%
        - 노출 클릭률: {ctr2:.1f}%

        3. 세 번째 영상:
        - 제목: {title3}
        - 썸네일: {thumbnail3}
        - 조회수: {view_count3:,}회 (채널 평균 대비 {view_ratio3:.1f}배)
        - 평균 조회율: {retention_rate3:.1f}%
        - 댓글 참여율: {comment_rate3:.2f}%
        - 좋아요 참여율: {like_rate3:.2f}%
        - 노출 클릭률: {ctr3:.1f}%
        """
    }
]

# 6. 썸네일 성과 분석
PROMPT_thumbnail = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 썸네일 성과를 분석하는 전문가입니다.
        가장 효과적인 썸네일들의 특징을 파악하고, 클릭률을 높이기 위한
        실질적인 개선 방안을 제시해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        클릭률이 가장 높은 3개의 썸네일 데이터입니다:

        1. 첫 번째 썸네일:
        - 제목: {title1}
        - 썸네일: {thumbnail1}
        - 조회수: {view_count1:,}회
        - 평균 조회율: {retention_rate1:.1f}%
        - 댓글 참여율: {comment_rate1:.2f}%
        - 좋아요 참여율: {like_rate1:.2f}%
        - 노출 클릭률: {ctr1:.1f}% (채널 평균 대비 {ctr_ratio1:.1f}배)

        2. 두 번째 썸네일:
        - 제목: {title2}
        - 썸네일: {thumbnail2}
        - 조회수: {view_count2:,}회
        - 평균 조회율: {retention_rate2:.1f}%
        - 댓글 참여율: {comment_rate2:.2f}%
        - 좋아요 참여율: {like_rate2:.2f}%
        - 노출 클릭률: {ctr2:.1f}% (채널 평균 대비 {ctr_ratio2:.1f}배)

        3. 세 번째 썸네일:
        - 제목: {title3}
        - 썸네일: {thumbnail3}
        - 조회수: {view_count3:,}회
        - 평균 조회율: {retention_rate3:.1f}%
        - 댓글 참여율: {comment_rate3:.2f}%
        - 좋아요 참여율: {like_rate3:.2f}%
        - 노출 클릭률: {ctr3:.1f}% (채널 평균 대비 {ctr_ratio3:.1f}배)
        """
    }
]

# 7. 업로드 주기 분석
PROMPT_upload_pattern = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 콘텐츠 업로드 전략을 분석하는 전문가입니다.
        업로드 패턴의 효과성을 평가하고, 시청자 확보를 위한 최적의 업로드 전략을 제안해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        업로드 패턴 데이터입니다:

        1. 월별 업로드 추이:
        {monthly_data} (최근 12개월)

        2. 업로드 주기:
        - 월평균 업로드: {monthly_uploads:.1f}개
        - 전체 영상 수: {video_count:,}개
        - 업로드 순위: 전체 {total_channels}개 중 {upload_rank}위
        
        3. 채널 참여도:
        - 구독자 참여율: {participation:.1f}%
        - 참여도 순위: 전체 {total_channels}개 중 {engagement_rank}위
        - 경쟁 채널 평균 참여율: {avg_participation:.1f}%

        """
    }
]

# 8. 채널 활성도 분석석
PROMPT_activity = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 전반적인 활성도를 분석하는 전문가입니다.
        구독자 참여도와 콘텐츠 효과성을 평가하고, 채널 성장을 위한 구체적인 조언을 제공해주세요.
        """
    },
    {
        "role": "user",
        "content": """
        채널 활성도 데이터입니다:

        1. 구독자/조회수 추세:
        - 구독자 그래프: {subscriber_graph} (최근 90일)
        - 일일 조회수 그래프: {daily_view_graph} (최근 90일)
        - 누적 조회수 그래프: {total_view_graph} (최근 90일)

        2. 채널 성과:
        - 채널 평균 조회수: {user_avg_view:,}회 (전체 {total_channels}개 중 {view_rank}위)
        - 경쟁 채널 평균 조회수: {competitor_avg_view:,}회
        - 조회수/구독자 비율: {view_subscriber_ratio:.1f}%

        3. 채널 특성:
        - 월평균 업로드 수: {monthly_upload_count}개
        - 구독자 참여도: {engagement_rate:.1f}% (전체 {total_channels}개 중 {engagement_rank}위)
        """
    }
]

PROMPT_summary = [
    {
        "role": "system",
        "content": """
        당신은 유튜브 채널의 종합적인 분석 결과를 전문가적 시각으로 요약하는 전략적 분석가입니다.
        오직 제공된 데이터만을 기반으로 분석해야 합니다.
        추가 정보나 가정을 만들어내지 마세요.
        오직 주어진 수치에 대해서만 간결하고 명확하게 분석하세요.

        """
    },
    {
        "role": "user",
        "content": """
        채널의 종합 데이터입니다:

        1. 수익성:
        - 월평균 조회수 수입: {view_income:,}원
        """
    }
]