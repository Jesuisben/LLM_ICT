"""
rag_example_01.py

카페 메뉴 문서를 SQLite DB에 저장
최초 1회 실행
"""

import os
import sqlite3


documents = [
    "이 카페의 아메리카노는 산미가 적고 고소한 맛이 특징이며, 달콤한 케이크와 잘 어울립니다.",
    "라떼는 고소한 우유와 에스프레소가 조화를 이루는 음료로, 부드러운 케이크와 함께 마시기 좋습니다.",
    "딸기 치즈케이크는 부드러운 식감과 상큼한 맛이 특징으로, 라떼나 아메리카노와 궁합이 좋습니다.",
    "초코 케이크는 달콤한 초콜릿 맛이 진한 디저트로, 쌉싸름한 커피 음료와 잘 어울립니다.",
    "크루아상은 버터 향이 풍부한 바삭한 빵으로, 아메리카노와 함께 즐기기 좋습니다."
]


DB_FILE = "data/cafe.db"

os.makedirs(
    "data",
    exist_ok=True
)


with sqlite3.connect(DB_FILE) as conn:

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        "DELETE FROM documents"
    )

    cursor.executemany(
        "INSERT INTO documents(content) VALUES(?)",
        [(doc,) for doc in documents]
    )


print("SQLite DB 생성 완료")
print(f"저장 위치 : {DB_FILE}")