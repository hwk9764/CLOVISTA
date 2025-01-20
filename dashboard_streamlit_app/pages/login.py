import streamlit as st
from .utils import login


# CSS로 사이드바 숨기기 함수
def hide_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_page(USER_DATA):
    """로그인 페이지"""
    st.markdown("<h1 style='text-align: center; color: white;'>Login to The AIluminator</h1>", unsafe_allow_html=True)

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if login(username_input, password_input, USER_DATA):
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.rerun()
        else:
            st.error("Invalid username or password.")
