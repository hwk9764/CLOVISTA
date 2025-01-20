import streamlit as st


def login(username, password, USER_DATA):
    """사용자 이름과 비밀번호를 확인하는 함수"""
    return username in USER_DATA and USER_DATA[username] == password


def logout():
    """로그아웃 함수"""
    st.session_state.logged_in = False
    st.session_state.username = None
