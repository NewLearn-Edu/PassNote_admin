import streamlit as st
import dashboard

st.set_page_config(
    page_title="패스노트 관리자 페이지",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 예시 사용자 정보 (실제 앱에선 DB 또는 환경변수 사용 추천)
USERS = {
    "웅진북센": "1234",
    "뉴런": "1234"
}

# 로그인 함수
def login(username, password):
    if username in USERS and USERS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("로그인 성공!")
        st.rerun()
    else:
        st.error("아이디 또는 비밀번호가 틀렸습니다.")

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# 로그인 상태 확인
if not st.session_state.get("logged_in", False):
    st.title("🔐 관리자 로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login(username, password)
else:
    st.sidebar.success(f"{st.session_state.username} 님, 환영합니다!")
    if st.sidebar.button("로그아웃"):
        logout()
    dashboard.show()