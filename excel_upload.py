import io
import zipfile
import streamlit as st
import numpy as np
import pandas as pd
import requests

API_BASE = "http://prod-alb-949821740.ap-northeast-2.elb.amazonaws.com"

def show():
    col_for_mac, col_for_window = st.columns(2)
    with col_for_mac:
        st.download_button(
            label="📥 암호화 실행기 for window",
            data=open("main.exe", 'rb').read(),  # 파일을 바이너리 모드로 읽어 data로 전달
            file_name="main.exe",  # 다운로드될 파일 이름
            mime="application/octet-stream"  # EXE 파일의 MIME 타입
        )

    st.subheader("📄 업로드 파일 업로드")
    col_excel, col_zip = st.columns(2)
    with col_excel:
        uploaded_excel = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"], key="excel")
    with col_zip:
        uploaded_zip = st.file_uploader(".zip 파일을 업로드하세요", type=["zip"], key="zip")

    if st.button("💾 저장하기"):
        if uploaded_excel is not None and uploaded_zip is not None:
            excel_bytes = uploaded_excel.read()

            unzip_file = unzip(uploaded_zip)

            response = upload(excel_bytes, unzip_file)
            
            if response is not None:
                st.success("✅ 구매내역이 세션에 저장되었습니다.")
            else:
                st.write(f"서버 응답: {response.status_code} {response.text}")

    if uploaded_excel is not None:
        try:
            df = pd.read_excel(uploaded_excel)
            st.markdown(f"### 📊 업로드된 엑셀 테이블 ({len(df)} 개)")
            st.dataframe(df)
        except Exception as e:
            st.error(f"엑셀 파일 처리 중 오류 발생: {e}")

def upload(excel_file: bytes, zip_files: list):
    url = f"{API_BASE}/upload"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 먼저 로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = [
        ("file", ("books.xlsx", excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
    ]
    for name, zip_file in zip_files:
        files.append(("zips", (name, zip_file, "application/zip")))

    response = requests.post(url, headers=headers, files=files)
    print(response.text)
    return response

def unzip(uploaded_zip):
    if uploaded_zip is not None:
        try:
            zip_file = zipfile.ZipFile(uploaded_zip)

            inner_zip_files = []
            for name in zip_file.namelist():
                if name.endswith(".zip"):
                    inner_data = zip_file.read(name)  # 내부 zip 파일의 바이트
                    inner_zip_files.append(inner_data)

            st.write(f"📦 내부 ZIP 파일 개수: {len(inner_zip_files)}개")
            return [(name, zip_file.read(name)) for name in zip_file.namelist() if name.endswith(".zip")]
        except Exception as e:
            st.error(f"압축 해제 중 오류 발생: {e}")
            return []
    return []