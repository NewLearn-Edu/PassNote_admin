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
        st.warning("구매내역이 없습니다.")

def fetch_purchase_history(api_url: str, token: str) -> pd.DataFrame:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.post(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}, {response.text}")

    data = response.json()  # 예: list of dicts

    # 예시 데이터에서 사용하는 컬럼 이름에 맞게 변환
    df = pd.DataFrame(data)
    
    if df.empty:
        df = pd.DataFrame(columns=["회원명", "도서명", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "memberName": "회원명",
        "bookName": "도서명",
        "price": "가격",
        "createdAt": "구매일",
        "isRefunded": "환불여부"
    }, inplace=True)

    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    
    return df