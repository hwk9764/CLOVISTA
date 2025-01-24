# -*- coding: utf-8 -*-
from prompt import PROMPT_performance, PROMPT_relation, PROMPT_revenue
from data_processing import import_from_db
import requests
import json
#import pandas as pd

class CompletionExecutor:
    def __init__(self, host, api_key, request_id):
        self._host = host
        self._api_key = api_key
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'Authorization': self._api_key,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        response_content = ""
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    if data.startswith("data:"):
                        json_data = json.loads(data[5:])
                        if "message" in json_data and "content" in json_data["message"]:
                            response_content = json_data["message"]["content"]
        print(response_content, end="")

if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='Bearer nv-f5786fde571f424786ed0823986ca992h3P1',
        request_id='309fa53d16a64d7c9c2d8f67f74ac70d'
    )

    channel_id = 0  # 분석할 채널 ID
    metrics = {
        'performance': import_from_db(channel_id, 1),
        'relation': import_from_db(channel_id, 2), 
        'revenue': import_from_db(channel_id, 3)
    }

    prompts = [PROMPT_performance, PROMPT_relation, PROMPT_revenue]
    prompt_names = ["performance", "relation", "revenue"]

    for prompt, name in zip(prompts, prompt_names):
        print(f"\n{'-'*20} {name} {'-'*20}")
        formatted_prompt = [
            prompt[0],
            {"role": "user", "content": prompt[1]['content'].format(**metrics[name])}
        ]
        request_data = {
            'messages': formatted_prompt,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 2000,
            'temperature': 0.15,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': False,
            'seed': 0
        }
        completion_executor.execute(request_data)