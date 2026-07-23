import sqlite3

DB_PATH = "database.db"

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1️⃣ products 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    # 2️⃣ 기존 데이터 제거 (실습 재실행 대비)
    cursor.execute("DELETE FROM products")

    # 3️⃣ 샘플 데이터 삽입
    products = [
        (1, 'Keyboard', 30000, 15),
        (2, 'Mouse', 15000, 40),
        (3, 'Monitor', 200000, 7),
        (4, 'USB Cable', 5000, 100),
    ]

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()

    print("✅ database.db 초기화 완료 (products 테이블 생성 및 데이터 삽입)")


if __name__ == "__main__":
    init_database()