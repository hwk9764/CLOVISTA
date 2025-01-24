PROMPT_performance = [
    {
        "role": "system",
        "content": "당신은 유튜브 채널 성과 분석 전문가입니다. 채널의 평균 조회수를 분석하세요."
    },
    {
        "role": "user",
        "content": "현재 채널 지표:\n- 평균 조회수: {avg_views}"
    }
]

PROMPT_relation = [
    {
        "role": "system",
        "content": "당신은 유튜브 채널 관계성 분석 전문가입니다. 라이브 방송 현황을 분석하세요."
    },
    {
        "role": "user",
        "content": "현재 채널 지표:\n- 라이브 방송 수: {live_count}회"
    }
]

PROMPT_revenue = [
    {
        "role": "system",
        "content": "당신은 유튜브 채널 수익성 분석 전문가입니다. 광고 영상 수를 분석하세요."
    },
    {
        "role": "user",
        "content": "현재 채널 지표:\n- 광고 영상 수: {sponsored_count}개"
    }
]