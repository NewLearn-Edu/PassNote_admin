import streamlit as st
import pandas as pd
import random

def show():
    st.subheader("🏠 홈")
    st.write("이곳은 관리자 홈 화면입니다.")
    st.info("필요한 요약 정보 또는 알림을 여기에 표시할 수 있습니다.")
    if "uploaded_excel_df" in st.session_state:
        df = st.session_state["uploaded_excel_df"].copy()
        if "노출" not in df.columns:
            df["노출"] = True

        # 무조건 10%는 False로 설정
        num_false = int(len(df) * 0.1)
        if num_false > 0:
            false_indices = random.sample(range(len(df)), num_false)
            df.loc[:, "노출"] = True
            df.loc[false_indices, "노출"] = False
        visible_books = df[df["노출"] == True]
        st.markdown(f"### ✅업데이트 된 책(판매중인 책 : {len(visible_books)}권)")
        edited_df = st.data_editor(df, num_rows="dynamic")
        st.session_state["uploaded_excel_df"] = edited_df
    else:
        st.warning("📁 업로드된 엑셀 파일이 없습니다. '엑셀 업로드' 탭에서 파일을 업로드하고 저장하세요.")