# python 설치시 기본으로 설치됨
import sqlite3

# 사용할 SQLite 데이터베이스 파일 이름
# 해당 파일이 없으면 연결할 때 새로 생성됨
DB_NAME = "database.db"

# 데이터베이스를 초기화하는 함수
def init_database():
    # SQLite 데이터베이스 파일에 연결
    # database.db가 없으면 현재 실행 위치에 새로 생성됨
    conn = sqlite3.connect(DB_NAME)

    # SQL문을 실행하기 위한 Cursor 객체 생성
    cursor = conn.cursor()

    # SQL문 실행
    # 상품(products) 테이블 생성
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    # 재실습을 위하여 기존 데이터 삭제
    cursor.execute("delete from products")

    # 샘플 데이터 추가
    items = [
        (1, 'Keyboard', 30000, 15),
        (2, 'Mouse', 15000, 40),
        (3, 'Monitor', 200000, 7),
        (4, 'USB Cable', 5000, 100),
    ]

    # executemany(sql, parameters) : 같은 SQL문을 여러 데이터에 반복 실행하는 함수
    # sql : 반복해서 실행할 하나의 SQL문
    # parameters : SQL문에 넣을 여러 데이터 묶음
    cursor.executemany(
        # ?를 placeholder라고 부름 (원래 html에서 입력상자 기본값으로도 사용)
        # ?가 무언가로 치환될 것이라고 말하는 것 (치환 대상 items의 내용들)
        #INSERT INTO products VALUES (1, 'Keyboard', 30000, 15);
        # INSERT INTO products VALUES (2, 'Mouse', 15000, 40);
        # INSERT INTO products VALUES (3, 'Monitor', 200000, 7);
        # INSERT INTO products VALUES (4, 'USB Cable', 5000, 100);
        "insert into products values(?, ?, ?, ?)",
        items
    )

    # 지금까지 실행한 INSERT, UPDATE, DELETE,
    # CREATE TABLE 등의 변경 내용을 데이터베이스에 최종 반영
    conn.commit()

    # 데이터베이스 연결 종료
    conn.close()

    print(f"{DB_NAME} 데이터베이스 생성 완료")

if __name__ == "__main__":
    init_database()