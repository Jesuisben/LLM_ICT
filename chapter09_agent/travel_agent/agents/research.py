from datetime import datetime

# from datetime import datetime
from langchain_core.messages import AIMessage

from chapter09_agent.travel_agent.state import State
from chapter09_agent.travel_agent.models.research_result import ResearchResult, FlightInfo, HotelInfo, WeatherInfo
from chapter09_agent.travel_agent.tools.airport_api import search_flight
from chapter09_agent.travel_agent.tools.weather_api import get_weather
from chapter09_agent.travel_agent.tools.hotel_api import search_hotel

def research_agent(state: State):
    print("\n===== research_agent 실행 =====")
    trip_plan = state["trip_plan"]

    departure = trip_plan.departure # 출발지
    destination = trip_plan.destination # 도착지
    departure_date = trip_plan.start_date # 출장 시작일

    flights  = search_flight(departure, destination, departure_date)

    # print(f"\n{sys._getframe().f_code.co_name}에서의 비행 정보 출력")
    # print(flights )

    # -------------------------------
    # 항공편
    # -------------------------------
    flight_infos = []

    if trip_plan.need_flight:
        flights = search_flight(
            departure,
            destination,
            departure_date
        )

        flight_infos = [
            FlightInfo(**flight)
            for flight in flights
        ]
    # end if

    # -------------------------------
    # 날씨
    # -------------------------------
    weather_infos = None

    if trip_plan.need_weather:
        weather = get_weather(
            destination=destination,
            target_date=trip_plan.start_date.replace("-", ""),
            base_date=datetime.today().strftime("%Y%m%d")
        )

        weather_infos = WeatherInfo(**weather)
    # end if

    # -------------------------------
    # 호텔
    # -------------------------------
    hotel_infos = []

    if trip_plan.need_hotel:
        hotels = search_hotel(
            destination=trip_plan.destination,
            check_in=trip_plan.start_date,
            check_out=trip_plan.end_date
        )

        hotel_infos = [
            HotelInfo(**hotel)
            for hotel in hotels
        ]
    # end if

    state["research_result"] = ResearchResult(
        flight_list=flight_infos,
        hotel_list=hotel_infos,
        weather=weather_infos
    )

    state["messages"].append(
        AIMessage("[Research] 조사 완료")
    )

    task = state["task_history"][-1]

    task.done = True

    return state
# end def research_agent