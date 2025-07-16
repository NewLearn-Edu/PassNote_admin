import streamlit as st
import pandas as pd
import requests

def show():
    st.subheader("👤 회원 목록")
    st.write("현재 등록된 회원 정보를 확인할 수 있습니다.")

    df = fetch_members()

    if not df.empty:
        st.markdown(f"### ✅ 총 회원 수: {len(df)}명")
        st.dataframe(df, use_container_width=True)
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