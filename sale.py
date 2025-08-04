import streamlit as st
import pandas as pd
import calendar
import requests

def show():
    st.subheader("📆 분기별 판매량")
    
    try:
        companytype = st.session_state.get("companytype")
        if companytype == "book":
            df = fetch_book_purchase_history()
        elif companytype == "template":
            df = fetch_template_purchase_history()
            
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return

    if df.empty:
        st.warning("구매내역 데이터가 없습니다.")

    df["구매일"] = pd.to_datetime(df["구매일"])
    df["년도"] = df["구매일"].dt.year
    df["월"] = df["구매일"].dt.month

    # 현재 연도 기준 필터링
    current_year = pd.Timestamp.today().year
    df = df[df["년도"] == current_year]
    
    options = {
        "1분기": [1, 2, 3],
        "2분기": [4, 5, 6],
        "3분기": [7, 8, 9],
        "4분기": [10, 11, 12],
        "상반기": [1, 2, 3, 4, 5, 6],
        "하반기": [7, 8, 9, 10, 11, 12],
        "전기": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }

    # 현재 달이 속한 분기 자동 선택
    current_month = pd.Timestamp.today().month
    default_period = None
    for key, months in options.items():
        if current_month in months:
            default_period = key
            break

    period = st.radio("기간 선택", list(options.keys()) + ["직접 기간 선택"], horizontal=True, index=list(options.keys()).index(default_period))

    if period != "직접 기간 선택":
        selected_months = options[period]
        start_month = min(selected_months)
        end_month = max(selected_months)

        # 시작일과 종료일 계산
        start_date = pd.Timestamp(f"{current_year}-{start_month:02d}-01")
        last_day = calendar.monthrange(current_year, end_month)[1]
        end_date = pd.Timestamp(f"{current_year}-{end_month:02d}-{last_day}")
    else:
        with st.expander("📅 기간 직접 선택"):
            start_date = st.date_input("시작일", value=pd.to_datetime(f"{current_year}-01-01"), key="start_date")
            end_date = st.date_input("종료일", value=pd.to_datetime(f"{current_year}-12-31"), key="end_date")

    if start_date and end_date:
        filtered_df = df[(df["구매일"] >= pd.to_datetime(start_date)) & (df["구매일"] <= pd.to_datetime(end_date))]
    else:
        filtered_df = pd.DataFrame()

    if not filtered_df.empty:
        st.markdown(f"### 📦 판매량 요약 ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})")
    else:
        st.markdown("### 📦 판매량 요약 (선택한 기간에 데이터가 없습니다.)")

    if filtered_df.empty:
        st.warning("선택한 기간에 해당하는 판매 데이터가 없습니다.")
        return

    st.write(f"총 판매 수: {len(filtered_df)}건")
    st.write(f"총 판매 금액: {filtered_df['가격'].sum():,}원")
    st.write(f"평균 책 가격: {filtered_df['가격'].mean():.2f}원")

    st.markdown("### 🧾 판매 테이블")
    st.dataframe(filtered_df)

    st.markdown("### 📊 월별 판매 건수")
    month_counts = filtered_df["월"].value_counts().sort_index()
    st.bar_chart(month_counts)

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
        df = pd.DataFrame(columns=["도서명", "출판사", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "bookName": "도서명",
        "publisher": "출판사",
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
        df = pd.DataFrame(columns=["속지명", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "templateName": "속지명",
        "price": "가격",
        "created_at": "구매일",
        "is_refunded": "환불여부"
    }, inplace=True)

    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    
    return df
