"""
Booking.com 호텔 검색 (Dummy Version)

실제 Booking API 대신 Dummy 데이터를 반환한다.
추후 Booking API를 연결할 경우 search_hotel() 내부만 수정하면 된다.
"""


from datetime import datetime, timedelta


########################################################################
# 목적지 ID 검색 (Dummy)
########################################################################

def get_destination_id(keyword: str):
    """
    도시명 -> Dummy Destination ID 반환
    """

    return {
        "dest_id": "dummy",
        "dest_type": "city",
        "name": keyword
    }


########################################################################
# 호텔 검색 (Dummy)
########################################################################

def search_hotel(
        destination: str,
        check_in: str,
        check_out: str
):
    """
    Dummy 호텔 검색

    Args:
        destination : 목적지
        check_in    : 체크인 날짜 (YYYY-MM-DD)
        check_out   : 체크아웃 날짜 (YYYY-MM-DD)

    Returns:
        호텔 정보 List
    """

    print(f"[Dummy] 호텔 검색")
    print(f"목적지 : {destination}")
    print(f"체크인 : {check_in}")
    print(f"체크아웃 : {check_out}")

    hotels = [

        {
            "hotel_name": f"{destination} 그랜드 호텔",
            "location": destination,
            "address": f"{destination}시 중앙로 100",
            "price": 120000,
            "total_price": 360000,
            "rating": 9.2,
            "room_type": "스탠다드 더블"
        },

        {
            "hotel_name": f"{destination} 비즈니스 호텔",
            "location": destination,
            "address": f"{destination}시 비즈니스로 25",
            "price": 95000,
            "total_price": 285000,
            "rating": 8.8,
            "room_type": "디럭스 싱글"
        },

        {
            "hotel_name": f"{destination} 시티 호텔",
            "location": destination,
            "address": f"{destination}시 시청길 10",
            "price": 150000,
            "total_price": 450000,
            "rating": 9.5,
            "room_type": "프리미엄 더블"
        },

        {
            "hotel_name": f"{destination} 리조트",
            "location": destination,
            "address": f"{destination}시 해변로 88",
            "price": 210000,
            "total_price": 630000,
            "rating": 9.7,
            "room_type": "오션뷰 스위트"
        }

    ]

    return hotels


########################################################################
# 테스트
########################################################################

if __name__ == "__main__":

    # 오늘 날짜
    check_in = datetime.today()

    # 3일 후
    check_out = check_in + timedelta(days=3)

    result = search_hotel(
        destination="제주",
        check_in=check_in.strftime("%Y-%m-%d"),
        check_out=check_out.strftime("%Y-%m-%d")
    )

    from pprint import pprint

    print("\n===== Dummy 호텔 검색 결과 =====")
    pprint(result)