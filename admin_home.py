import streamlit as st
import pandas as pd
import requests
import demo_mode

def show():
    st.markdown("### ✅ 관리자 통계 요약")
    demo_mode.show_demo_banner()

    data = fetch_admin_statistics()
    if not data:
        print("nodata???")
        return

    # 총 회원 수
    total_members = data["totalMembers"]
    current_members = data["currentMembers"]
    delete_members = data["deleteMembers"]
    st.write(f"👥 누적 가입자 수: {total_members}명")
    st.write(f"👥 현 회원 수: {current_members}명")
    st.write(f"👥 회원탈퇴 수: {delete_members}명")
    total_charge_point = data["totalChargePoint"]
    st.write(f"🔋 총 충전 금액: {total_charge_point:,}원")

    # 총 판매 중인 책 수
    total_books = data["totalBooks"]
    st.write(f"📚 총 판매 중인 책 수: {total_books}권")

    # 총 판매 중인 속지 수
    total_templates = data["totalTemplates"]
    st.write(f"📄 총 판매 중인 속지 수: {total_templates}개")

    # 총 판매된 책 금액
    total_book_sales = data["totalBookSales"]
    st.write(f"💰 총 판매된 책 금액: {total_book_sales:,}원")

    # 총 판매된 속지 금액
    total_template_sales = data["totalTemplateSales"]
    st.write(f"💰 총 판매된 속지 금액: {total_template_sales:,}원")

    # 업체별 판매된 책 금액
    st.markdown("### 🏢 업체별 책 판매 금액")
    book_sales_by_company = pd.DataFrame(data["bookSalesByCompany"])
    st.dataframe(book_sales_by_company)

    # 업체별 판매된 속지 금액
    st.markdown("### 🏢 업체별 속지 판매 금액")
    template_sales_by_company = pd.DataFrame(data["templateSalesByCompany"])
    st.dataframe(template_sales_by_company)

def fetch_admin_statistics() -> pd.DataFrame:
    if demo_mode.is_demo_mode():
        return demo_mode.get_demo_admin_statistics()

    API_BASE = st.session_state.get("API_BASE")
    url = f"{API_BASE}/admin/statistics"

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

    return data
