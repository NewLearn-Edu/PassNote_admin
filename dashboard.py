import streamlit as st
import home
import user
import sale
import excel_upload

def show():
    st.title("📊 관리자 대시보드")

    # 사이드바 내비게이션
    if  st.session_state.get("username") == "sognodigitalhub":
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량"])
    else: 
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량", "책 업로드"])
    
    if menu == "홈":
        home.show()
    elif menu == "사용자 통계":
        user.show()
    elif menu == "분기별 판매량":
        sale.show()
    elif menu == "책 업로드":
        excel_upload.show()