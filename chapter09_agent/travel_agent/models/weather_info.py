from pydantic import BaseModel, Field


class WeatherInfo(BaseModel):
    """날씨 정보"""

    location: str = Field(default="", description="지역")
    weather: str = Field(default="", description="날씨")

    temperature: float = Field(default=0.0, description="기온")
    humidity: float = Field(default=0.0, description="습도")

    rain_probability: float = Field(default=0.0, description="강수확률")
    wind_speed: float = Field(default=0.0, description="풍속")

    def __str__(self):
        return (
            f"""
지역 : {self.location}
날씨 : {self.weather}
기온 : {self.temperature:.1f}℃
습도 : {self.humidity:.0f}%
강수확률 : {self.rain_probability:.0f}%
풍속 : {self.wind_speed:.1f} m/s
"""
        )

    def __repr__(self):
        return self.__str__()