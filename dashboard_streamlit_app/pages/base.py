import streamlit as st
from .utils import logout


def render_base_page(LOGO_PATH):
    t1, t2 = st.columns((0.07, 1))
    t1.image(LOGO_PATH, width=120)
    t2.title("The AIluminator")
    t2.markdown(
        " **[Visit Homepage](https://imlabswu.notion.site/The-AIluminator-1605f153c3fa80739373f8e30ee1681b?pvs=74)**",
        unsafe_allow_html=True,
    )

    # 사이드바 설정
    with st.sidebar:
        st.sidebar.success(f"Welcome {st.session_state.username}!")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()
