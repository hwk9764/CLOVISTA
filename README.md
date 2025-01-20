# 🔥 네이버 AI Tech NLP 8조 The AIluminator 🌟
## Level 4 Hackathon


# Installation and Quick Start
**Step 1.** 프로젝트에 필요한 모든 dependencies는 `requirements.txt`에 있고, 이에 대한 가상환경을 생성해서 프로젝트를 실행
```sh
# 가상환경 만들기
$ python -m venv .venv

# 가상환경 켜기
$ . .venv/bin/activate

# 제공되는 서버 환경에 따라 선택적 사용
$ export TMPDIR=/data/ephemeral/tmp 
$ mkdir -p $TMPDIR

# 필요 라이브러리 설치
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


## Running the Application
### Setup the API Backend
```sh
uvicorn restapi.router:app --host 0.0.0.0 --port 8000
```
### Setup the Streamlit UI
```sh
streamlit run dashboard_streamlit_app/app.py
```

### Access the Chatbot
Open your browser and navigate to the following address to interact with the chatbot :
```sh
http://localhost:8501
```

### Login Credentials
- Use the following credentials to log in and test the application :
    - User 1 :
        - ID : `user1`
        - Password : `1234`
    - User 2 :
        - ID : `user2`
        - Password : `5678`