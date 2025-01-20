import os
import streamlit as st
from pages import hide_sidebar, render_login_page, render_base_page

# 환경 변수 설정
BASEDIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASEDIR, "images", "logo.png")

# 데모용 사용자 데이터
USER_DATA = {"user1": "1234", "user2": "1234"}

# 페이지 설정
st.set_page_config(page_title="The AIluminator", layout="wide", page_icon=":ambulance:")

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None


def main():
    """메인 함수"""
    if not st.session_state.logged_in:
        hide_sidebar()
        render_login_page(USER_DATA)
    else:
        render_base_page(LOGO_PATH)


if __name__ == "__main__":
    main()
