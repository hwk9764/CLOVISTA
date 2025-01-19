# -*- coding: utf-8 -*-
from prompt import PROMPT
import requests
import json
import pandas as pd

class CompletionExecutor:
   def __init__(self, host, api_key, api_key_primary_val, request_id):
       self._host = host
       self._api_key = api_key
       self._api_key_primary_val = api_key_primary_val
       self._request_id = request_id

   def execute(self, completion_request):
       headers = {
           'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
           'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
           'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
           'Content-Type': 'application/json; charset=utf-8',
           'Accept': 'text/event-stream'
       }
       full_response = ""
    
       try:
            with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                        headers=headers, json=completion_request, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")
                        if decoded_line.startswith('data:'):
                            try:
                                json_data = json.loads(decoded_line[5:])
                                if 'message' in json_data and 'content' in json_data['message']:
                                    # 응답을 누적
                                    full_response = json_data['message']['content']
                            except json.JSONDecodeError:
                                continue
                
                # 루프가 끝난 후 한 번만 출력
                print(full_response)
       except Exception as e:
           print(f"Error: {str(e)}")

def import_from_db(csv_path,channel_name):
    """
    DB 의 ROW를 읽어와서 PROMPT 에 필요한 리스트를 생성합니다.

    Parameters:
        csv_path (str): CSV 파일 경로. (추후에 DB에서 읽어올 수 있게 변경할 예정)

    Returns:
        list: PROMPT의 {}에 삽입할 데이터를 포함한 리스트.

    """
    df=pd.read_csv(csv_path)
    target_row = df[df['channel']==channel_name].iloc[0]
    return target_row

if __name__ == '__main__':
   
   completion_executor = CompletionExecutor(
       host='https://clovastudio.stream.ntruss.com',
       api_key='NTA0MjU2MWZlZTcxNDJiY6vj3yrjLz6x2b+0YLV8dZWaraw1NtqTzIpT66gshJzS',
       api_key_primary_val='G79Y59rzKfdIolOUkB7b3Skx1vDHWamsdA4UV9uo',
       request_id='89b4665b4ccb4535a0a79d251ae77bc2'
   )

   prompt_format=import_from_db("prs_cns/test_db.csv","빠더너스 BDNS")

   request_data = {
    #    'messages': "안녕하세요",
       'messages': [
            PROMPT[0], 
            {"role": "user", "content": PROMPT[1]['content'].format(*prompt_format)}
        ],
       'topP': 0.8,
       'topK': 0,
       'maxTokens': 500,
       'temperature': 0.15,
       'repeatPenalty': 5.0,
       'stopBefore': [],
       'includeAiFilters': False,
       'seed': 0
   }
   completion_executor.execute(request_data)