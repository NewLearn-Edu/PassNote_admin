import streamlit as st
import pandas as pd

def show():
    st.subheader("📈 사용자 통계")
    
    if "uploaded_excel_df" in st.session_state and "purchase_table" in st.session_state:
        df = st.session_state["uploaded_excel_df"].copy()
        purchase_table = st.session_state["purchase_table"].copy()
        
        purchase_counts = purchase_table["책이름"].value_counts().reset_index()
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
        st.warning("업로드된 데이터 또는 구매내역이 없습니다. '엑셀 업로드' 탭에서 파일을 업로드하고 저장하세요.")
