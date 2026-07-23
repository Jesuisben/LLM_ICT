import sqlite3

DB_PATH = "database.db"

def get_product_info(product_id: int, field: str):
    """
    상품 ID와 조회할 항목(name, price, stock)을 받아 결과 반환
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"SELECT {field} FROM products WHERE product_id = ?"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return f"{field}: {result[0]}"
    else:
        return "상품을 찾을 수 없습니다."


def add_product(name: str, price: int, stock: int):
    """
    새로운 상품을 DB에 추가
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )

    conn.commit()
    conn.close()

    return f"상품 추가 완료: {name} / {price}원 / 재고 {stock}개"


get_product_info_tool = {
    "type": "function",
    "function": {
        "name": "get_product_info",
        "description": "상품 정보를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "integer",
                    "description": "상품 번호"
                },
                "field": {
                    "type": "string",
                    "description": "조회할 항목 (name, price, stock)"
                }
            },
            "required": ["product_id", "field"]
        }
    }
}

add_product_tool = {
    "type": "function",
    "function": {
        "name": "add_product",
        "description": "새로운 상품을 추가합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "상품명"
                },
                "price": {
                    "type": "integer",
                    "description": "단가"
                },
                "stock": {
                    "type": "integer",
                    "description": "재고 수량"
                }
            },
            "required": ["name", "price", "stock"]
        }
    }
}

tools = [
    get_product_info_tool,
    add_product_tool
]
