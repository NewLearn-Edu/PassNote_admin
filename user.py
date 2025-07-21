import streamlit as st
import pandas as pd
import requests

def show():
    st.subheader("📈 사용자 통계")

    companytype = st.session_state.get("companytype")

    if companytype == "book":
        df = fetch_book_purchase_history()
    elif companytype == "template":
        df = fetch_template_purchase_history()
    else:
        st.error("알 수 없는 companytype입니다.")
        df = pd.DataFrame()  # 빈 데이터프레임 처리

    total_sales = len(df)
    total_revenue = df["가격"].sum()
    free_user_count = (df["가격"] == 0).sum()

    st.markdown(f"**총 판매 수량:** {total_sales:,}권")
    st.markdown(f"**무료 제공 수:** {free_user_count:,}권")
    st.markdown(f"**총 판매 금액:** {int(total_revenue):,}")


    st.markdown("### 🧾 구매 기록 테이블")
    st.dataframe(df)

    # 판매량 분석
    label = "도서명" if companytype == "book" else "속지명"
    title_prefix = "책" if companytype == "book" else "속지"

    st.markdown(f"### 🏆 {title_prefix} 판매량")

    sales = df.groupby(label).size().reset_index(name="판매량")
    sorted_items = sales.sort_values(by="판매량", ascending=False)

    top_n = st.slider(f"그래프에 표시할 상위 {title_prefix} 개수", min_value=1, max_value=len(sorted_items), value=10)

    st.markdown(f"#### 🏆 많이 팔린 {title_prefix} TOP {top_n}")
    st.dataframe(sorted_items.head(top_n))

    sorted_items_for_chart = sorted_items.set_index(label)
    st.bar_chart(sorted_items_for_chart.head(top_n))

def fetch_book_purchase_history() -> pd.DataFrame:
    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/books/purchases"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 재로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}, {response.text}")

    data = response.json()  # 예: list of dicts

    # 예시 데이터에서 사용하는 컬럼 이름에 맞게 변환
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("구매내역이 없습니다.")
        df = pd.DataFrame(columns=["회원명", "도서명", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "memberName": "회원명",
        "bookName": "도서명",
        "price": "가격",
        "created_at": "구매일",
        "is_refunded": "환불여부"
    }, inplace=True)

    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    
    return df

def fetch_template_purchase_history() -> pd.DataFrame:
    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/template/purchases"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 재로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}, {response.text}")

    data = response.json()  # 예: list of dicts

    # 예시 데이터에서 사용하는 컬럼 이름에 맞게 변환
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("구매내역이 없습니다.")
        df = pd.DataFrame(columns=["회원명", "속지명", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "memberName": "회원명",
        "templateName": "속지명",
        "price": "가격",
        "created_at": "구매일",
        "is_refunded": "환불여부"
    }, inplace=True)

    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    
    return df