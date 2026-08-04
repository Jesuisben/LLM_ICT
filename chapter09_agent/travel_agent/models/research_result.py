from typing import Optional

from typing import List

from pydantic import BaseModel, Field

from chapter09_agent.travel_agent.models.flight_info import FlightInfo
from chapter09_agent.travel_agent.models.hotel_info import HotelInfo
from chapter09_agent.travel_agent.models.weather_info import WeatherInfo


class ResearchResult(BaseModel):
    """조사 결과"""

    flight_list: List[FlightInfo] = Field(default_factory=list)

    hotel_list: List[HotelInfo] = Field(default_factory=list)

    weather: Optional[WeatherInfo] = None

    def __str__(self):

        result = []

        result.append("[항공편]")

        if not self.flight_list:
            result.append("없음")

        for index, flight in enumerate(self.flight_list, start=1):

            result.append(
                f"""
{index}. {flight.airline} {flight.flight_number}
   출발 : {flight.departure}
   도착 : {flight.arrival}
   출발 공항 : {flight.departure_airport}
   도착 공항 : {flight.arrival_airport}
   예정 시간 : {flight.scheduled_time}
   예상 시간 : {flight.estimated_time}
   상태 : {flight.status}
"""
            )

        result.append("\n[호텔]")

        if not self.hotel_list:
            result.append("없음")
        else:
            for index, hotel in enumerate(self.hotel_list, start=1):
                result.append(
                    f"""
{index}. {hotel.name}
   위치 : {hotel.location}
   가격 : {hotel.price:,.0f}원
   평점 : {hotel.rating}
"""
                )

        result.append("\n[날씨]")
        result.append(str(self.weather))

        return "\n".join(result)