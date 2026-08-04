from pydantic import BaseModel, Field

class TripPlan(BaseModel):
    """출장 계획 정보"""

    departure: str = Field(
        default="",
        description="출장 출발지"
    )

    destination: str = Field(
        default="",
        description="출장 목적지"
    )

    start_date: str = Field(
        default="",
        description="출장 시작일"
    )

    end_date: str = Field(
        default="",
        description="출장 종료일"
    )

    period: str = Field(
        default="",
        description="출장 기간"
    )

    need_flight: bool = Field(
        default=True,
        description="항공편 예약 필요 여부"
    )

    need_hotel: bool = Field(
        default=True,
        description="호텔 예약 필요 여부"
    )

    need_weather: bool = Field(
        default=True,
        description="날씨 정보 조사 필요 여부"
    )

    summary: str = Field(
        default="",
        description="출장 계획 요약"
    )

    def __str__(self):
        return (
            f"출발지 : {self.departure}\n"
            f"도착지 : {self.destination}\n"
            f"출장 시작일 : {self.start_date}\n"
            f"출장 종료일 : {self.end_date}\n"
            f"출장 기간 : {self.period}\n"
            f"항공편 예약 필요 여부 : {self.need_flight}\n"
            f"호텔 예약 필요 여부 : {self.need_hotel}\n"
            f"날씨 정보 조사 필요 여부 : {self.need_weather}\n"
            f"출장 계획 요약 : {self.summary}"
        )

    # Pydantic(BaseModel)은 자체적으로 __repr__()을 가지고 있기 때문에
    # 여러분이 만든 __str__()가 아니라 Pydantic의 출력 형식을 사용합니다.
    def __repr__(self):
        return self.__str__()
# end class TripPlan