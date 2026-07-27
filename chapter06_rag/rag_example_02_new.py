import sqlite3


def load_documents(db_path):
    """ documents 테이블에서 문서(Document) 조회 """

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            select content from documents order by id
        """)

        all_content = cursor.fetchall()

        # cursor.fetchall()로 데이터 베이스의 데이터를 가져옴
        # 데이터 베이스를 가져오면 튜플로 처리해서 0번째가 진짜 데이터여서 [0]이라고 적음
        # all_content 내부 : [("이 카페의 아메리카노는 산미가 적고 고소한 맛이 특징이며, 달콤한 케이크와 잘 어울립니다.", ), ...]
        return [row[0] for row in all_content]

def print_documents(documents):
    print("문서 목록")
    for idx, doc in enumerate(documents, 1):
        print(f"[{idx}] {doc}")

DB_FILE = "data/cafe.db"

if __name__ == "__main__":
    docs = load_documents(DB_FILE)

    print_documents(docs)