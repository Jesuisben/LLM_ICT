import sqlite3

DB_NAME = "database.db"

#############################################################
# LLM이 호출하여 실제 동작을 수행하는 함수
#############################################################

# 사용자 : 상품 1의 이름과 단가를 알려줘
def get_product_info(product_id: int, field: str):
    """
    상품 ID와 조회할 항목(name, price, stock)을 받아 결과 반환
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = f"SELECT {field} FROM products WHERE product_id = ?"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    print("get_product_info 함수 결과")
    print(result)

    conn.close()

    if result:
        return f"상품 번호 {product_id}의 필드 {field}의 반환 값 {result}"
    else:
        return "상품을 찾을 수 없습니다."

# 사용자 : 10만원짜리 하드 디스크 HDD를 10개 추가하는 코드 작성
def add_product(name: str, price: int, stock: int):
    """
    새로운 상품을 DB에 추가
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )

    conn.commit()
    conn.close()

    return f"상품 추가 완료: {name} / {price}원 / 재고 {stock}개"
#############################################################
# 툴에 대한 명세표
#############################################################
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
#############################################################
# LLM에게 전달해줄 Tool List
#############################################################
tool_list = [
    get_product_info_tool,
    add_product_tool
]