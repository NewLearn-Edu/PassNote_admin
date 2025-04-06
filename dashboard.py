import streamlit as st
import zipfile
from io import BytesIO
import pandas as pd
import io
from sample_data import sample_data
import numpy as np
import random

def show():
    st.title("📊 관리자 대시보드")

    # 사이드바 내비게이션
    menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "기간별 판매량", "엑셀 업로드"])

    if menu == "홈":
        show_home()
    elif menu == "사용자 통계":
        show_user_stats()
    elif menu == "기간별 판매량":
        show_sale_stats()
    elif menu == "엑셀 업로드":
        show_excel_upload()

def show_home():
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

def show_user_stats():
    st.subheader("📈 사용자 통계")
    
    if "uploaded_excel_df" in st.session_state:
        df = st.session_state["uploaded_excel_df"].copy()
        
        purchase_table = pd.DataFrame({
            "구매자": [f"사용자{i+1}" for i in range(len(df))],
            "구매한책": df["책이름"].sample(frac=1, replace=True).reset_index(drop=True),
            "가격": [random.randint(10000, 30000) for _ in range(len(df))],
            "구매일": pd.date_range(end=pd.Timestamp.today(), periods=len(df)).strftime("%Y-%m-%d")
        })
        purchase_counts = purchase_table["구매한책"].value_counts().reset_index()
        purchase_counts.columns = ["책이름", "구매수"]
        df = df.merge(purchase_counts, on="책이름", how="left")
        df["구매수"] = df["구매수"].fillna(0).astype(int)

        st.write(f"총 판매량: {df['구매수'].sum():,}권")
        st.write(f"평균 판매량: {df['구매수'].mean():.2f}권")
        st.write(f"중간값: {df['구매수'].median()}권")
        st.write(f"최댓값: {df['구매수'].max()}권 / 최솟값: {df['구매수'].min()}권")

        if "노출" in df.columns:
            visible_avg = df[df["노출"] == True]["구매수"].mean()
            hidden_avg = df[df["노출"] == False]["구매수"].mean()
            st.write(f"노출된 책 평균 판매량: {visible_avg:.2f}권")
            st.write(f"숨겨진 책 평균 판매량: {hidden_avg:.2f}권")

        st.markdown("### 🧾 구매 기록 테이블")
        st.dataframe(purchase_table)

        # Removed old title markdown; will add updated title after top_n is defined.
        st.markdown(f"### 🏆 책 판매량")
        top_books = df.groupby("책이름")["구매수"].sum().reset_index()
        sorted_books = top_books.sort_values(by="구매수", ascending=False)
        
        top_n = st.slider("그래프에 표시할 상위 책 개수", min_value=1, max_value=len(sorted_books), value=10)
        
        st.markdown(f"#### 🏆 많이 팔린 책 TOP {top_n}")
        st.dataframe(sorted_books.head(top_n))

        sorted_books_for_chart = sorted_books.set_index("책이름")
        st.bar_chart(sorted_books_for_chart.sort_values(by="구매수", ascending=False).head(top_n))

    else:
        st.warning("업로드된 데이터가 없습니다. '엑셀 업로드' 탭에서 파일을 업로드하고 저장하세요.")

def show_sale_stats():
    st.subheader("🏠 분기별 판매량")

def show_excel_upload():
    import io

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        sample_data.to_excel(writer, index=False, sheet_name="샘플")
    buffer.seek(0)

    col_download, col_save, _ = st.columns([1, 1, 5])
    with col_download:
        st.download_button(
            label="📥 엑셀 형식 다운로드",
            data=buffer,
            file_name="sample_format.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

                # 기존 df를 새 Excel로 저장하고, 구매내역 시트 추가
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="책 데이터")
                    purchase_data.to_excel(writer, index=False, sheet_name="구매내역")
                buffer.seek(0)

                st.download_button(
                    label="📥 구매내역 포함된 엑셀 저장",
                    data=buffer,
                    file_name="book_with_purchases.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.success("📁 데이터와 구매내역이 저장되었습니다! 다운로드 버튼을 통해 저장하세요.")
            else:
                st.warning("❗ 먼저 엑셀 파일을 업로드해주세요.")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📂 엑셀 업로드")
        uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"], key="excel")
    
    with col2:
        st.subheader("🗜️ ZIP 파일 업로드")
        uploaded_zip = st.file_uploader("ZIP 파일을 업로드하세요", type=["zip"], key="zip")
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            expected_columns = sample_data.columns.tolist()
            uploaded_columns = df.columns.tolist()
            if expected_columns != uploaded_columns:
                st.warning("⚠️ 업로드된 파일의 컬럼이 샘플 형식과 다릅니다. 형식을 확인해주세요.")
            st.markdown(f"### 📊 업로드된 엑셀 테이블 ({len(df)} 개)")
            st.dataframe(df)

            st.session_state["uploaded_excel_df"] = df
            
        except Exception as e:
            st.error(f"파일을 읽는 중 오류 발생: {e}")

    if uploaded_zip is not None:
        try:
            with zipfile.ZipFile(BytesIO(uploaded_zip.read())) as zf:
                file_list = zf.namelist()
                st.success(f"ZIP 파일에 {len(file_list)}개의 파일이 포함되어 있습니다.")
                st.write("📂 포함된 파일 목록:")
                for f in file_list:
                    st.write(f"- {f}")

                excel_files = [f for f in file_list if f.endswith(".xlsx")]
                st.markdown(f"### 📑 총 {len(excel_files)}개의 엑셀 파일")
                for file_name in excel_files:
                    with zf.open(file_name) as file:
                        try:
                            df = pd.read_excel(file)
                            st.markdown(f"#### 📄 {file_name}")
                            st.dataframe(df)
                        except Exception as e:
                            st.error(f"{file_name} 파일을 읽는 중 오류 발생: {e}")
        except Exception as e:
            st.error(f"{file_name} 파일을 읽는 중 오류 발생: {e}")