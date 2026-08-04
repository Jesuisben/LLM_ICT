'''
다음 코드는 "한국공항공사_실시간 항공기 운항정보 조회_GW"에 대한 크롤링을 위한 코드입니다.
잘못된 것이 있으면 수정해주세요
'''

import os, sys
import requests

from chapter09_agent.travel_agent.constant.constants import AIRPORTS
from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
SERVICE_KEY = get_api_key(find_api)

SERVICE_KEY = os.getenv("DATA_GO_API_KEY")

if not SERVICE_KEY:
    raise ValueError(
        "API KEY 환경 변수가 존재하지 않습니다."
    )

def search_flight(
        departure: str,
        destination: str,
        departure_date: str,
        adults: int = 1
):
    """
    한국공항공사 실시간 항공기 운항정보 조회

    Args:
        departure : 출발 공항명, 예) 서울, 김포
        destination : 도착 공항명, 예) 제주
        departure_date : 조회 날짜, 예) 2026-08-01
        adults : 탑승 인원(호환성을 위한 파라미터)

    Returns:
        항공 운항 정보 리스트
    """

    url = (
        "https://apis.data.go.kr/B551178/flight-status" + '/info'
    )

    '''
    한국공항공사_실시간 항공기 운항정보 조회_GW 페이지 확인
    https://www.data.go.kr/iim/api/selectAPIAcountView.do
    https://data.go.kr/data/15158625/openapi.do
    '''
    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "type": "json",
        "from_time": "0000",
        "to_time": "2400",
        "airport": AIRPORTS[departure],
        "schLineType":"D",
        "schAirCode":AIRPORTS[destination],
        "schIOType":'I' # 출발과 도착을 동시 지정할 수 없음(배타적)
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    # print("\nURL :", response.url)
    # print("\nSTATUS :", response.status_code)

    # print('응답 JSON')
    # print(f'\n{response.text}')

    # response.raise_for_status()

    data = response.json()
    # print(data)

    flights = []

    items = (
        data
        .get("response", {})
        .get("body", {})
        .get("items", {})
        .get("item", [])
    )
    print(f"\n{sys._getframe().f_code.co_name}에서 수행됨")
    print(f'필터링 전 운행 회수 : {len(items)}')

    for item in items:
        if item.get('airport') == AIRPORTS[destination] and item.get('city') == AIRPORTS[departure]:
            flight = {
                "flight_number": item.get("airFln"),
                "airline": item.get("airlineKorean"),
                "departure": item.get("boardingKor"),
                "arrival": item.get("arrivedKor"),
                "departure_airport": item.get("city"),
                "arrival_airport": item.get("airport"),
                "scheduled_time": item.get("std"),
                "estimated_time": item.get("etd"),
                "status": item.get("rmkKor"),
                "status_eng": item.get("rmkEng"),
                "gate": item.get("gate"),
                "line": item.get("line"),
                "io": item.get("io")
            }

            flights.append(flight)
        # end if

    print(f"\n{sys._getframe().f_code.co_name}에서 수행됨")
    print(f'최종 필터링된 운행 회수 : {len(flights)}\n')
    return flights
########################################################################
# 테스트
########################################################################
from datetime import datetime
from pprint import pprint

if __name__ == "__main__":

    today = datetime.today().strftime("%Y-%m-%d")

    result = search_flight(
        departure="김포",
        destination="제주",
        departure_date=today
    )

    print("최종 반환값")
    pprint(result)
########################################################################