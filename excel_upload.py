import io
import zipfile
import streamlit as st
import numpy as np

def show():
    with open("sample_format.zip", "rb") as f:
        zip_buffer = io.BytesIO(f.read())

    col_download, col_save, _ = st.columns([1, 1, 5])
    with col_download:
        st.download_button(
            label="📥 엑셀 형식 다운로드",
            data=zip_buffer,
            file_name="sample_format.zip",
            mime="application/zip"
        )
    with col_save:
        if st.button("💾 저장하기"):
            if "uploaded_excel_df" in st.session_state:
                df = st.session_state["uploaded_excel_df"].copy()

                # 구매내역 데이터 생성
                num_records = 1000
                purchase_data = pd.DataFrame({
                    "구매자": [f"사용자{i % 100 + 1}" for i in range(num_records)],
                    "책이름": [random.choice(df["책이름"].tolist()) for _ in range(num_records)],
                })
                purchase_data["가격"] = purchase_data["책이름"].map(df.set_index("책이름")["가격"])
                purchase_data["구매일"] = pd.to_datetime(np.random.choice(pd.date_range(start="2024-01-01", end="2025-04-06"), num_records)).strftime("%Y-%m-%d")

                # 세션 상태에 저장
                st.session_state["purchase_table"] = purchase_data

                st.success("✅ 구매내역이 세션에 저장되었습니다.")
            else:
                st.warning("❗ 먼저 엑셀 파일을 업로드해주세요.")
    
    st.subheader("📄 엑셀 파일 업로드")
    uploaded_excel = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"], key="excel")

    if uploaded_excel is not None:
        try:
            df = pd.read_excel(uploaded_excel)
            st.markdown(f"### 📊 업로드된 엑셀 테이블 ({len(df)} 개)")
            st.dataframe(df)
            st.session_state["uploaded_excel_df"] = df
        except Exception as e:
            st.error(f"엑셀 파일 처리 중 오류 발생: {e}")