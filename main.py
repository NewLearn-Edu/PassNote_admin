import streamlit as st
import requests
import dashboard

API_BASE = "http://prod-alb-949821740.ap-northeast-2.elb.amazonaws.com"

st.set_page_config(
    page_title="패스노트 관리자 페이지",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 로그인 함수
def login(username, password):
    url = f"{API_BASE}/distributor/login"
    try:
        response = requests.post(url, json={
            "email": username,
            "password": password
        })
        if response.status_code == 200 and "distributorToken" in response.cookies:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.token = response.cookies["distributorToken"]
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("로그인 실패: 잘못된 정보 또는 서버 오류")
    except Exception as e:
        st.error(f"로그인 중 오류 발생: {e}")

# 로그아웃 함수
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.token = ""
    st.rerun()

# 로그인 상태 확인
if not st.session_state.get("logged_in", False):
    st.title("🔐 관리자 로그인")
    username = st.text_input("아이디 (이메일)")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login(username, password)
else:
    st.sidebar.success(f"{st.session_state.username} 님, 환영합니다!")
    if st.sidebar.button("로그아웃"):
        logout()
    dashboard.show()