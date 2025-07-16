import streamlit as st
import home
import user
import sale
import excel_upload
import members  # members.py를 만든 경우

def show():
    st.title("📊 관리자 대시보드")

    user_name = st.session_state.get("username")
    
    # 사이드바 메뉴 설정
    if user_name == "sognodigitalhub":
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량"])
    elif user_name == "newlearn":
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "회원 목록"])
    else: 
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량", "책 업로드"])
    
    # 메뉴에 따른 화면 분기
    if menu == "홈":
        home.show()
    elif menu == "사용자 통계":
        user.show()
    elif menu == "분기별 판매량":
        sale.show()
    elif menu == "책 업로드":
        excel_upload.show()
    elif menu == "회원 목록":
        members.show()