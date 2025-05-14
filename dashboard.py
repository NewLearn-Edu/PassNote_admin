import streamlit as st
import home
import user
import sale
import excel_upload

def show():
    st.title("📊 관리자 대시보드")

    # 사이드바 내비게이션
    menu = st.sidebar.radio("📂 메뉴 선택", ["홈", "사용자 통계", "분기별 판매량", "엑셀 업로드"])
    print(st.session_state.get("username"))
    if menu == "홈":
        home.show()
    elif menu == "사용자 통계":
        user.show()
    elif menu == "분기별 판매량":
        sale.show()
    elif menu == "엑셀 업로드" and st.session_state.get("username") != "songodigitalhub":
        excel_upload.show()