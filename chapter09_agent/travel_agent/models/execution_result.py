from typing import Optional

from pydantic import BaseModel, Field

from chapter09_agent.travel_agent.models.flight_info import FlightInfo
from chapter09_agent.travel_agent.models.hotel_info import HotelInfo
from chapter09_agent.travel_agent.models.weather_info import WeatherInfo


class ExecutionResult(BaseModel):
    """Executor가 계산한 최종 결과"""

    flight: Optional[FlightInfo] = None

    hotel: Optional[HotelInfo] = None

    weather: Optional[WeatherInfo] = None

    flight_price: float = Field(
        default=0.0,
        description="항공권 가격"
    )

    hotel_price: float = Field(
        default=0.0,
        description="숙박비"
    )

    total_cost: float = Field(
        default=0.0,
        description="총 비용"
    )