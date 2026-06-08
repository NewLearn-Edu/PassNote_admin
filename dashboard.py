import streamlit as st
import home
import user
import sale
import excel_upload
import members  # members.py를 만든 경우
import admin_home
import pushNotification

def show():
    st.title("📊 관리자 대시보드")

    companytype = st.session_state.get("companytype")
    
    # 사이드바 메뉴 설정
    if companytype == "template":
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량"])
    elif companytype == "admin":
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "회원 목록", "푸시알림 보내기"])
    else: 
        menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량", "책 업로드"])
    
    # 메뉴에 따른 화면 분기
    if menu == "홈":
        if companytype == "admin":
            admin_home.show()
        else:
            home.show()
    elif menu == "푸시알림 보내기":
        pushNotification.show()
    elif menu == "사용자 통계":
        user.show()
    elif menu == "분기별 판매량":
        sale.show()
    elif menu == "책 업로드":
        excel_upload.show()
    elif menu == "회원 목록":
        members.show()
