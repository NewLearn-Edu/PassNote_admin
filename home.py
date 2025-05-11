import streamlit as st
import pandas as pd
import random
import requests

API_BASE = "http://prod-alb-949821740.ap-northeast-2.elb.amazonaws.com"

def show():
    st.subheader("🏠 홈")
    st.write("이곳은 관리자 홈 화면입니다.")
    st.info("필요한 요약 정보 또는 알림을 여기에 표시할 수 있습니다.")
    
    df = fetch_books_by_company()
    
    if not df.empty:
        visible_books = df[df["공개여부"] == True]

        st.markdown(f"### ✅업데이트 된 책(판매중인 책 : {len(visible_books)}권)")
        edited_df = st.data_editor(df, num_rows="dynamic")
        st.session_state["uploaded_excel_df"] = edited_df
    else:
        st.warning("📁 업로드된 엑셀 파일이 없습니다. '엑셀 업로드' 탭에서 파일을 업로드하고 저장하세요.")

def fetch_books_by_company():
    url = f"{API_BASE}/api/books/company"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 먼저 로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        st.error(f"도서 정보를 가져오지 못했습니다. 상태 코드: {response.status_code}")
        return pd.DataFrame()

    books = response.json()

    df = pd.DataFrame(books)
    
    if df.empty:
        df = pd.DataFrame(columns=["회원명", "도서명", "가격", "구매일", "환불여부"])
        return df

    df.rename(columns={
        "name": "도서명",
        "description": "설명",
        "price": "가격",
        "publicationDate": "출판일",
        "author": "저자",
        "publisher": "출판사",
        "isPublic": "공개여부",
        "isbn": "ISBN",
        "pages": "쪽수"
    }, inplace=True)

    return df[["도서명", "설명", "가격", "출판일", "저자", "출판사", "공개여부", "ISBN", "쪽수"]]