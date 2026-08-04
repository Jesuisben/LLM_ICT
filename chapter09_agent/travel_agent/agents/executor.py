from datetime import datetime

from chapter09_agent.travel_agent.models.execution_result import ExecutionResult
from chapter09_agent.travel_agent.state import State
from chapter09_agent.travel_agent.models.flight_info import FlightInfo
from chapter09_agent.travel_agent.models.hotel_info import HotelInfo
from chapter09_agent.travel_agent.models.weather_info import WeatherInfo

def executor_agent(state: State):

    print("\n===== EXECUTOR =====")

    research = state["research_result"]

    flight = (
        research.flight_list[0]
        if research.flight_list
        else None
    )

    hotel = (
        research.hotel_list[0]
        if research.hotel_list
        else None
    )

    weather = research.weather if research.weather else None

    flight_price = (
        flight.price
        if flight
        else 0
    )

    hotel_price = (
        hotel.total_price
        if hotel
        else 0
    )

    total_cost = (
        flight_price +
        hotel_price
    )

    state["execution_result"] = ExecutionResult(

        flight=flight,

        hotel=hotel,

        weather=weather,

        flight_price=flight_price,

        hotel_price=hotel_price,

        total_cost=total_cost
    )

    task = state["task_history"][-1]

    task.done = True

    task.done_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return state