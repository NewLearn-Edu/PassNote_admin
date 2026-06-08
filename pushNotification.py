import streamlit as st
import requests
import demo_mode

def show():
    st.markdown("## 🔔 푸시 알림 전송")
    demo_mode.show_demo_banner()

    # 제목과 내용 입력
    title = st.text_input("제목을 입력하세요")
    message = st.text_area("내용을 입력하세요")

    # 앱 선택 (다중 선택)
    app_options = {
        "패스노트": "passnote",
        "한국사": "koreanhistory",
        "한능검": "koreanhistoryexam",
        "경찰학": "policescience"
    }
    selected_apps = st.multiselect("앱을 선택하세요", options=list(app_options.keys()))

    if st.button("✅ 푸시 전송"):
        if not title or not message or not selected_apps:
            st.warning("제목, 내용, 앱을 모두 입력해주세요.")
            return

        if demo_mode.is_demo_mode():
            for app_kor in selected_apps:
                st.success(f"[{app_kor}] 테스트 전송 미리보기 완료")
            return

        API_BASE = st.session_state.get("API_BASE")
        token = st.session_state.get("token")

        if not token:
            st.error("세션 토큰이 없습니다. 다시 로그인해주세요.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        for app_kor in selected_apps:
            app_eng = app_options[app_kor]
            url = f"{API_BASE}/notification/send/{app_eng}"
            payload = {
                "title": title,
                "message": message
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 201 or response.status_code == 200:
                st.success(f"[{app_kor}] 푸시 전송 완료")
            else:
                st.error(f"[{app_kor}] 푸시 전송 실패: {response.status_code} {response.text}")
