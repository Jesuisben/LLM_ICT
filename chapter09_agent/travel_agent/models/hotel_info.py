from pydantic import BaseModel, Field


class HotelInfo(BaseModel):
    """호텔 정보"""

    # 기본 정보
    name: str = Field(default="", description="호텔명")
    location: str = Field(default="", description="호텔 위치")
    address: str = Field(default="", description="호텔 주소")

    # 호텔 정보
    property_class: int = Field(default=0, description="호텔 등급(성급)")

    # 가격
    price: float = Field(default=0.0, description="1박 가격")
    total_price: float = Field(default=0.0, description="총 숙박 가격")
    currency: str = Field(default="KRW", description="통화")

    # 평점
    rating: float = Field(default=0.0, description="호텔 평점")
    rating_text: str = Field(default="", description="평점 설명")
    review_count: int = Field(default=0, description="리뷰 개수")

    # 객실
    room_type: str = Field(default="", description="객실 타입")

    # 일정
    check_in: str = Field(default="", description="체크인 날짜")
    check_out: str = Field(default="", description="체크아웃 날짜")

    # 위치
    latitude: float = Field(default=0.0, description="위도")
    longitude: float = Field(default=0.0, description="경도")

    # 사진
    photo_url: str = Field(default="", description="대표 사진")

    def __str__(self):
        return (
            f"""
호텔명 : {self.name}
호텔 등급 : {self.property_class}성급

위치 : {self.location}
주소 : {self.address}

객실 : {self.room_type}

체크인 : {self.check_in}
체크아웃 : {self.check_out}

1박 가격 : {self.price:,.0f} {self.currency}
총 가격 : {self.total_price:,.0f} {self.currency}

평점 : {self.rating} ({self.rating_text})
리뷰 수 : {self.review_count:,}개

위도 : {self.latitude}
경도 : {self.longitude}

대표 사진 : {self.photo_url}
"""
        )

    def __repr__(self):
        return self.__str__()