import io
import zipfile
import streamlit as st
import numpy as np
import pandas as pd
import requests

def show():
    col_for_window, col_for_mac = st.columns(2)

    with col_for_window:
        st.download_button(
            label="📥 암호화 실행기 for Window",
            data=open("make_for_window.exe", 'rb').read(),  # 파일을 바이너리 모드로 읽어 data로 전달
            file_name="make_for_window.exe",  # 다운로드될 파일 이름
            mime="application/octet-stream"  # EXE 파일의 MIME 타입
        )

    # with col_for_mac:
    #     st.download_button(
    #         label="📥 암호화 실행기 for Mac",
    #         data=open("make_for_mac.zip", 'rb').read(),  # 파일을 바이너리 모드로 읽어 data로 전달
    #         file_name="make_for_mac.zip",  # 다운로드될 파일 이름
    #         mime="application/octet-stream"  # EXE 파일의 MIME 타입
    #     )

    st.subheader("📄 업로드 파일 업로드")
    col_excel, col_zip = st.columns(2)
    with col_excel:
        uploaded_excel = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"], key="excel")
    with col_zip:
        uploaded_zip = st.file_uploader(".zip 파일을 업로드하세요", type=["zip"], key="zip")

    if uploaded_excel is not None:
        try:
            df = pd.read_excel(uploaded_excel)
            df["Description"] = df["Description"].fillna(" ")
            # df["PublicationDate"] = df["PublicationDate"].astype(str)
            df["PublicationDate"] = pd.to_datetime(df["PublicationDate"].astype(str), format="%Y-%m-%d", errors='coerce')
            st.markdown(f"### 📊 업로드된 엑셀 테이블 ({len(df)} 개)")
            st.dataframe(df, use_container_width=True)

            if uploaded_zip is not None and st.button("💾 저장하기"):
                excel_chunks = [df.iloc[[i]] for i in range(len(df))] # [df[i:i+5] for i in range(0, len(df), 5)]
                progress_bar = st.progress(0)
                total = len(excel_chunks)

                unzip_files = unzip(uploaded_zip)
                for i, chunk in enumerate(excel_chunks):
                    buffer = io.BytesIO()
                    chunk.to_excel(buffer, index=False)
                    buffer.seek(0)
                    chunk_bytes = buffer.read()

                    # name 컬럼이 있는 경우만 처리
                    if "Name" not in chunk.columns:
                        st.warning("name 컬럼이 없습니다. 업로드를 건너뜁니다.")
                        continue

                    names_in_chunk = chunk["Name"].astype(str).tolist()

                    # name과 일치하는 unzip_file 필터링
                    filtered_zip_files = [(name, content) for name, content in unzip_files if any(n in name for n in names_in_chunk)]
                    response = upload(chunk_bytes, filtered_zip_files)

                    progress_bar.progress(int((i + 1) / total * 100))
                
                st.success("✅ 일부 세션이 저장되었습니다.")
        except Exception as e:
            st.error(f"엑셀 파일 처리 중 오류 발생: {e}")

def upload(excel_file: bytes, zip_files: list):
    API_BASE = st.session_state.get("API_BASE")
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
        files.append(("file", (name, zip_file, "application/zip")))

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

            return [(name, zip_file.read(name)) for name in zip_file.namelist() if name.endswith(".zip")]
        except Exception as e:
            st.error(f"압축 해제 중 오류 발생: {e}")
            return []
    return []
