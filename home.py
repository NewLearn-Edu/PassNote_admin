import streamlit as st
import pandas as pd
import requests
import demo_mode

def show():
    st.subheader("🏠 홈")
    demo_mode.show_demo_banner()
    st.write("이곳은 관리자 홈 화면입니다.")
    
    companytype = st.session_state.get("companytype")
    if companytype == "book":
        df = fetch_books_by_company()
    elif companytype == "template":
        df = fetch_template_by_company()
    
    if not df.empty:
        visible_books = df[df["공개여부"] == True]

        label = "책" if companytype == "book" else "속지"
        st.markdown(f"### ✅업데이트 된 {label}(판매중인 {label} : {len(visible_books)}개)")
        st.dataframe(df)
    else:
        st.warning("📁 업로드 내역이 없습니다.")

def fetch_books_by_company():
    if demo_mode.is_demo_mode():
        return demo_mode.get_demo_books()

    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/books/company"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 재로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"도서 정보를 가져오지 못했습니다. 상태 코드: {response.status_code}")
        return pd.DataFrame()

    books = response.json()

    df = pd.DataFrame(books)
    
    if df.empty:
        df = pd.DataFrame(columns=["도서명", "가격", "구매일", "환불여부"])
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

def fetch_template_by_company():
    if demo_mode.is_demo_mode():
        return demo_mode.get_demo_templates()

    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/template/company"

    token = st.session_state.get("token")
    if not token:
        st.error("토큰이 세션에 존재하지 않습니다. 재로그인하세요.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        st.error(f"도서 정보를 가져오지 못했습니다. 상태 코드: {response.status_code}")
        return pd.DataFrame()

    books = response.json()

    df = pd.DataFrame(books)
    
    if df.empty:
        df = pd.DataFrame(columns=["속지명", "가격", "업로드일", "판매자명", "카테고리", "공개여부"])
        return df

    df.rename(columns={
        "name": "속지명",
        "price": "가격",
        "created_at": "업로드일",
        "seller": "판매자명",
        "category": "카테고리",
        "isPublic": "공개여부"
    }, inplace=True)

    return df[["속지명", "가격", "업로드일", "판매자명", "카테고리", "공개여부"]]
