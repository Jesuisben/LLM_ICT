"""
rag_example_02.py

SQLite 문서 조회 유틸리티
"""

import sqlite3

def load_documents(db_path):
    """SQLite documents 테이블에서 문서 조회"""

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT content
            FROM documents
            ORDER BY id
            """
        )
        # content 컬럼의 정보를 문자열 list로 반환합니다.
        return [row[0] for row in cursor.fetchall()]


def print_documents(documents):
    """문서 출력"""

    print("\n" + "=" * 50)
    print("문서 목록")
    print("=" * 50)

    for i, doc in enumerate(documents, 1):
        print(f"[{i}] {doc}")


if __name__ == "__main__":
    docs = load_documents("data/cafe.db")

    print_documents(docs)