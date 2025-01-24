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

# DB 수동 실행 (비번 0104)
$ su - postgres
$ /usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main
$ psql -h 10.28.224.177 -p 30634 -U postgres


# 필요 라이브러리 설치
$ https://blog.secretmuse.net/?p=380
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


## Running the Application
### Setup the API Backend
```sh
uvicorn rest_api.api:app --host 0.0.0.0 --port 30635 --reload
```