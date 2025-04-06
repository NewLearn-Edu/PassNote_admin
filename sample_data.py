import pandas as pd

sample_data = pd.DataFrame({
    "책이름": [f"ex) 샘플 도서 {i}" for i in range(1, 1001)],
    "책소개": [f"이것은 샘플 도서 {i}의 소개입니다." for i in range(1, 1001)],
    "저자": [f"저자{i}" for i in range(1, 1001)],
    "출판사": [f"출판사{i%10}" for i in range(1, 1001)],
    "출판일자": [f"2023-01-{(i%28)+1:02}" for i in range(1, 1001)],
    "가격": [10000 + (i * 10) for i in range(1, 1001)],
    "쪽수": [100 + (i % 300) for i in range(1, 1001)],
    "isbn": [f"9788998139{i:04}" for i in range(1, 1001)]
})
