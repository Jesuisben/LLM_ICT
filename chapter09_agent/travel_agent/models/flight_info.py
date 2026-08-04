from pydantic import BaseModel, Field


class FlightInfo(BaseModel):
    """항공편 정보"""

    price: float = Field(default=12345.0, description="항공권 가격")

    flight_number: str = Field(default="", description="편명")
    airline: str = Field(default="", description="항공사")

    departure: str = Field(default="", description="출발지")
    arrival: str = Field(default="", description="도착지")

    departure_airport: str = Field(default="", description="출발 공항 코드")
    arrival_airport: str = Field(default="", description="도착 공항 코드")

    scheduled_time: str = Field(default="", description="예정 시각")
    estimated_time: str = Field(default="", description="변경 시각")

    status: str = Field(default="", description="운항 상태")
    status_eng: str = Field(default="", description="운항 상태(영문)")

    gate: str = Field(default="", description="게이트")
    line: str = Field(default="", description="국내/국제")
    io: str = Field(default="", description="출도착 구분")

    @property
    def route(self): # 파생 컬럼 : 항공 노선
        return f"{self.departure} → {self.arrival}"

    def __str__(self):
        return (
            f"출발 : {self.departure}\n"
            f"도착 : {self.arrival}\n"
            f"출발 공항 : {self.departure_airport}\n"
            f"도착 공항 : {self.arrival_airport}\n"
            f"예정 시간 : {self.scheduled_time}\n"
            f"예상 시간 : {self.estimated_time}\n"
            f"상태 : {self.status}\n"
            f"탑승구 : {self.gate}"
        )

    def __repr__(self):
        return self.__str__()