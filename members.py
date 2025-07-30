import streamlit as st
import pandas as pd
import requests
import datetime

def show():
    st.subheader("👤 회원 목록")
    st.write("현재 등록된 회원 정보를 확인할 수 있습니다.")

    df = fetch_members()

    if not df.empty:
        st.markdown(f"### ✅ 총 회원 수: {len(df)}명")

        # 👉 직렬별 수 출력
        st.markdown("### 📚 직렬별 회원 수")
        career_counts = df["직렬"].value_counts().reset_index()
        career_counts.columns = ["직렬", "회원 수"]
        st.dataframe(career_counts, use_container_width=True)

        # 👉 전체 회원 테이블 출력
        st.markdown("### 📋 전체 회원 정보")
        st.dataframe(df, use_container_width=True)

        # 👉 일별 가입자 수 선그래프
        today = datetime.date.today()
        one_month_ago = today - datetime.timedelta(days=30)

        # 👉 최근 한 달간 가입자만 필터링
        df_recent = df[df["가입일자"].dt.date >= one_month_ago]

        # 👉 일별 가입자 수 집계
        df_daily = df_recent["가입일자"].dt.date.value_counts().sort_index()
        df_daily = df_daily.rename_axis("가입일").reset_index(name="가입자 수")

        # 👉 선그래프 출력
        st.markdown("### 📈 최근 한 달간 일별 가입자 수 추이")
        st.line_chart(df_daily.set_index("가입일"))
    else:
        st.warning("🙅 회원 정보가 없습니다.")

def fetch_members():
    url = "http://localhost:3000/members"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"회원 정보를 가져오지 못했습니다. 상태 코드: {response.status_code}")
            return pd.DataFrame()

        members = response.json()
        df = pd.DataFrame(members)

        if df.empty:
            return pd.DataFrame(columns=["ID", "이메일", "이름", "닉네임", "직렬", "이미지", "포인트", "가입일자"])

        df.rename(columns={
            "memberId": "ID",
            "email": "이메일",
            "name": "이름",
            "nickname": "닉네임",
            "target_career": "직렬",
            "animal_image": "이미지",
            "point": "포인트",
            "created_at": "가입일자"
        }, inplace=True)

        df["가입일자"] = pd.to_datetime(df["가입일자"])
        return df[["ID", "이메일", "이름", "닉네임", "직렬", "이미지", "포인트", "가입일자"]]

    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 실패: {e}")
        return pd.DataFrame()