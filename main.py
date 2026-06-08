import streamlit as st
import requests
import dashboard
import demo_mode

st.session_state["API_BASE"] = "http://localhost:3000" # "https://api.newlearn-soft.com"  # "http://pass-note-test-292308915.ap-northeast-2.elb.amazonaws.com"

# "http://localhost:3000"
# "https://api.newlearn-soft.com"
# "http://prod-alb-949821740.ap-northeast-2.elb.amazonaws.com"
# "http://pass-note-test-292308915.ap-northeast-2.elb.amazonaws.com/"

st.set_page_config(
    page_title="패스노트 관리자 페이지",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 로그인 함수
def login(username, password):
    demo_account = demo_mode.get_demo_account(username)
    if demo_account:
        if password != demo_mode.DEMO_PASSWORD:
            st.error(f"테스트 계정 비밀번호는 {demo_mode.DEMO_PASSWORD} 입니다.")
            return

        demo_mode.activate_demo_login(username, demo_account)
        st.success("테스트 계정으로 로그인했습니다. 더미 데이터를 표시합니다.")
        st.rerun()

    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/distributor/login"
    try:
        response = requests.post(url, json={
            "email": username,
            "password": password
        })

        if response.status_code == 200 and "distributorToken" in response.cookies:
            response_data = response.json()
            st.session_state.logged_in = True
            st.session_state.username = response_data.get("name")
            st.session_state.token = response.cookies["distributorToken"]
            st.session_state.companytype = response_data.get("type")
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
    demo_mode.clear_demo_session()
    st.rerun()

# 로그인 상태 확인
if not st.session_state.get("logged_in", False):
    st.title("🔐 관리자 로그인")
    username = st.text_input("아이디 (이메일)")
    password = st.text_input("비밀번호", type="password")

    with st.expander("테스트 계정 예시 보기"):
        st.write(f"공통 비밀번호: `{demo_mode.DEMO_PASSWORD}`")
        for email, companytype, name in demo_mode.get_demo_accounts_help():
            st.write(f"- `{email}` | `{companytype}` | {name}")

    if st.button("로그인"):
        login(username, password)
else:
    st.sidebar.success(f"{st.session_state.username} 님, 환영합니다!")
    if st.sidebar.button("로그아웃"):
        logout()
    dashboard.show()
