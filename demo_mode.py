import pandas as pd
import streamlit as st

DEMO_PASSWORD = "test1234"

DEMO_ACCOUNTS = {
    "test-book@passnote.local": {
        "name": "도서 테스트 계정",
        "type": "book",
        "company": "테스트 출판사",
    },
    "test-template@passnote.local": {
        "name": "속지 테스트 계정",
        "type": "template",
        "company": "테스트 속지 스토어",
    },
    "test-admin@passnote.local": {
        "name": "관리자 테스트 계정",
        "type": "admin",
        "company": "패스노트 운영팀",
    },
}

COMPANYTYPE_LABELS = {
    "book": "도서",
    "template": "속지",
    "admin": "관리자",
}


def get_demo_account(username: str):
    if not username:
        return None
    return DEMO_ACCOUNTS.get(username.strip().lower())


def activate_demo_login(username: str, account: dict):
    st.session_state.logged_in = True
    st.session_state.username = account["name"]
    st.session_state.token = "demo-token"
    st.session_state.companytype = account["type"]
    st.session_state.company = account["company"]
    st.session_state.is_test_account = True
    st.session_state.test_account_email = username.strip().lower()


def clear_demo_session():
    for key in ("is_test_account", "test_account_email", "company", "companytype"):
        if key in st.session_state:
            del st.session_state[key]


def is_demo_mode() -> bool:
    return bool(st.session_state.get("is_test_account"))


def show_demo_banner():
    if not is_demo_mode():
        return

    companytype = st.session_state.get("companytype")
    label = COMPANYTYPE_LABELS.get(companytype, companytype)
    st.info(f"테스트 {label} 계정으로 로그인되어 있습니다. 이 화면은 DB 조회 대신 더미 데이터로 표시됩니다.")


def get_demo_accounts_help():
    return [
        (email, account["type"], account["name"])
        for email, account in DEMO_ACCOUNTS.items()
    ]


def get_demo_books() -> pd.DataFrame:
    current_year = pd.Timestamp.today().year
    return pd.DataFrame(
        [
            {
                "도서명": "패스노트 행정법 압축집",
                "설명": "핵심 판례와 조문만 빠르게 정리한 도서",
                "가격": 22000,
                "출판일": f"{current_year}-01-15",
                "저자": "뉴런 편집부",
                "출판사": "테스트 출판사",
                "공개여부": True,
                "ISBN": "9791190000001",
                "쪽수": 312,
            },
            {
                "도서명": "패스노트 교육학 문제집",
                "설명": "기출 기반 실전 문제집",
                "가격": 18000,
                "출판일": f"{current_year}-02-28",
                "저자": "이정리",
                "출판사": "테스트 출판사",
                "공개여부": True,
                "ISBN": "9791190000002",
                "쪽수": 248,
            },
            {
                "도서명": "패스노트 한국사 요약집",
                "설명": "업로드 검수 중인 비공개 샘플",
                "가격": 15000,
                "출판일": f"{current_year}-03-12",
                "저자": "김정리",
                "출판사": "테스트 출판사",
                "공개여부": False,
                "ISBN": "9791190000003",
                "쪽수": 196,
            },
        ]
    )


def get_demo_templates() -> pd.DataFrame:
    current_year = pd.Timestamp.today().year
    return pd.DataFrame(
        [
            {
                "속지명": "합격 루틴 플래너",
                "가격": 3900,
                "업로드일": f"{current_year}-01-10",
                "판매자명": "테스트 속지 스토어",
                "카테고리": "플래너",
                "공개여부": True,
            },
            {
                "속지명": "과목별 오답노트",
                "가격": 2900,
                "업로드일": f"{current_year}-02-14",
                "판매자명": "테스트 속지 스토어",
                "카테고리": "학습관리",
                "공개여부": True,
            },
            {
                "속지명": "주간 회고 템플릿",
                "가격": 0,
                "업로드일": f"{current_year}-03-03",
                "판매자명": "테스트 속지 스토어",
                "카테고리": "무료배포",
                "공개여부": False,
            },
        ]
    )


def get_demo_book_purchase_history() -> pd.DataFrame:
    current_year = pd.Timestamp.today().year
    df = pd.DataFrame(
        [
            {"도서명": "패스노트 행정법 압축집", "출판사": "테스트 출판사", "가격": 22000, "구매일": f"{current_year}-01-08 10:30:00", "환불여부": 0},
            {"도서명": "패스노트 교육학 문제집", "출판사": "테스트 출판사", "가격": 18000, "구매일": f"{current_year}-01-20 14:12:00", "환불여부": 0},
            {"도서명": "패스노트 행정법 압축집", "출판사": "테스트 출판사", "가격": 22000, "구매일": f"{current_year}-02-05 09:20:00", "환불여부": 0},
            {"도서명": "패스노트 한국사 요약집", "출판사": "테스트 출판사", "가격": 15000, "구매일": f"{current_year}-03-11 21:05:00", "환불여부": 1},
            {"도서명": "패스노트 교육학 문제집", "출판사": "테스트 출판사", "가격": 18000, "구매일": f"{current_year}-04-02 08:45:00", "환불여부": 0},
            {"도서명": "패스노트 행정법 압축집", "출판사": "테스트 출판사", "가격": 22000, "구매일": f"{current_year}-04-07 19:40:00", "환불여부": 0},
        ]
    )
    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    return df


def get_demo_template_purchase_history() -> pd.DataFrame:
    current_year = pd.Timestamp.today().year
    df = pd.DataFrame(
        [
            {"속지명": "합격 루틴 플래너", "가격": 3900, "구매일": f"{current_year}-01-03 07:10:00", "환불여부": 0},
            {"속지명": "과목별 오답노트", "가격": 2900, "구매일": f"{current_year}-01-26 22:14:00", "환불여부": 0},
            {"속지명": "합격 루틴 플래너", "가격": 3900, "구매일": f"{current_year}-02-18 13:05:00", "환불여부": 0},
            {"속지명": "주간 회고 템플릿", "가격": 0, "구매일": f"{current_year}-03-09 12:30:00", "환불여부": 0},
            {"속지명": "과목별 오답노트", "가격": 2900, "구매일": f"{current_year}-03-28 17:42:00", "환불여부": 0},
            {"속지명": "합격 루틴 플래너", "가격": 3900, "구매일": f"{current_year}-04-05 09:05:00", "환불여부": 1},
        ]
    )
    df["구매일"] = pd.to_datetime(df["구매일"])
    df["가격"] = pd.to_numeric(df["가격"], errors="coerce")
    return df


def get_demo_admin_statistics() -> dict:
    return {
        "totalMembers": 12840,
        "currentMembers": 12104,
        "deleteMembers": 736,
        "totalChargePoint": 248900000,
        "totalBooks": 84,
        "totalTemplates": 156,
        "totalBookSales": 183500000,
        "totalTemplateSales": 65200000,
        "bookSalesByCompany": [
            {"업체명": "테스트 출판사", "판매금액": 48200000},
            {"업체명": "미래교육", "판매금액": 39100000},
            {"업체명": "합격연구소", "판매금액": 27500000},
        ],
        "templateSalesByCompany": [
            {"업체명": "테스트 속지 스토어", "판매금액": 18200000},
            {"업체명": "스터디메이커", "판매금액": 15100000},
            {"업체명": "러닝랩", "판매금액": 9400000},
        ],
    }


def get_demo_members() -> pd.DataFrame:
    current_year = pd.Timestamp.today().year
    df = pd.DataFrame(
        [
            {"ID": 1001, "이메일": "alpha@example.com", "이름": "김하나", "닉네임": "한걸음", "직렬": "교육학", "이미지": "fox", "포인트": 5200, "가입일자": f"{current_year}-03-11"},
            {"ID": 1002, "이메일": "beta@example.com", "이름": "이둘", "닉네임": "기출러", "직렬": "행정법", "이미지": "cat", "포인트": 8400, "가입일자": f"{current_year}-03-18"},
            {"ID": 1003, "이메일": "gamma@example.com", "이름": "박셋", "닉네임": "플래너왕", "직렬": "한국사", "이미지": "bear", "포인트": 1200, "가입일자": f"{current_year}-03-27"},
            {"ID": 1004, "이메일": "delta@example.com", "이름": "최넷", "닉네임": "루틴메이커", "직렬": "교육학", "이미지": "rabbit", "포인트": 3000, "가입일자": f"{current_year}-04-01"},
            {"ID": 1005, "이메일": "epsilon@example.com", "이름": "정다섯", "닉네임": "암기천재", "직렬": "행정법", "이미지": "dog", "포인트": 9600, "가입일자": f"{current_year}-04-06"},
        ]
    )
    df["가입일자"] = pd.to_datetime(df["가입일자"])
    return df
