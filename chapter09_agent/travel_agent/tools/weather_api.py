"""
공공데이터포털
기상청 단기예보 조회 API

인증키 발급
https://www.data.go.kr/iim/api/selectApiKeyList.do

사전 준비
1. https://www.data.go.kr
2. 기상청_단기예보 조회서비스 활용 신청
3. API Key 발급


https://www.data.go.kr/data/15084084/openapi.do
"""

import os
import requests
from pathlib import Path

from utility.env_util import get_api_key

find_api = "DATA_GO_API_KEY"
SERVICE_KEY = get_api_key(find_api)

if not SERVICE_KEY:
    raise ValueError("DATA_GO_API_KEY 환경 변수가 없습니다.")

# 현재 파일
CURRENT_DIR = Path(__file__).resolve().parent

# 상위 디렉터리
BASE_DIR = CURRENT_DIR.parent

# data 디렉터리
DATA_DIR = BASE_DIR / "data"

# data 폴더가 없으면 생성
DATA_DIR.mkdir(exist_ok=True)

# 저장 파일
LOG_FILE = DATA_DIR / "weather_log.txt"


# 지역 -> 기상청 격자 좌표
GRID = {
    "서울": (60, 127),
    "인천": (55, 124),
    "수원": (60, 121),
    "대전": (67, 100),
    "대구": (89, 90),
    "부산": (98, 76),
    "광주": (58, 74),
    "울산": (102, 84),
    "제주": (52, 38)
}


def get_weather(
        destination: str,
        target_date: str,
        base_date: str,
        base_time: str = "0800"
):
    """
    기상청 단기예보 조회

    Parameters
    ----------
    destination : 지역명
    target_date : 조회 날짜 (YYYYMMDD)
    base_date : 발표 날짜 (YYYYMMDD)
    base_time : 발표 시간
    """

    if destination not in GRID:
        raise ValueError(f"지원하지 않는 지역입니다. : {destination}")

    nx, ny = GRID[destination]

    url = (
        "https://apis.data.go.kr/1360000/"
        "VilageFcstInfoService_2.0/getVilageFcst"
    )

    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    header = data["response"]["header"]

    if header["resultMsg"] == "NO_DATA":
        raise ValueError("예보 데이터가 존재하지 않습니다.")

    items = data["response"]["body"]["items"]["item"]

    weather = ""
    temperature = None

    # 앞으로 사용할 값들
    humidity = None
    rain_probability = None
    wind_speed = None

    weather_map = {
        "1": "맑음",
        "3": "구름많음",
        "4": "흐림"
    }

    for item in items:

        if item["fcstDate"] != target_date:
            continue

        if item["fcstTime"] != "1200":
            continue

        category = item["category"]

        if category == "TMP":
            temperature = float(item["fcstValue"])

        elif category == "SKY":
            weather = weather_map.get(
                item["fcstValue"],
                "알수없음"
            )

        elif category == "REH":
            humidity = float(item["fcstValue"])

        elif category == "POP":
            rain_probability = float(item["fcstValue"])

        elif category == "WSD":
            wind_speed = float(item["fcstValue"])

    result = {
        "location": destination,
        "weather": weather,
        "temperature": temperature,
        "humidity": humidity,
        "rain_probability": rain_probability,
        "wind_speed": wind_speed
    }

    # ----------------------------------------------------
    # Console 출력
    # ----------------------------------------------------
    log = f"""
    ============================================================
    기상청 단기 예보 조회
    ============================================================
    조회 지역 : {destination}
    조회 날짜 : {target_date}
    발표 날짜 : {base_date}
    발표 시각 : {base_time}

    HTTP 응답 코드 : {response.status_code}

    ===== 응답 Header =====
    resultCode : {header["resultCode"]}
    resultMsg  : {header["resultMsg"]}

    ===== 12시 예보 =====
    기온 : {temperature:.1f}℃
    하늘상태 : {weather}
    습도 : {humidity}%
    강수확률 : {rain_probability}%
    풍속 : {wind_speed} m/s

    ===== Travel Agent 반환 데이터 =====
    {result}
    ============================================================

    """

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log)

    return result


##########################################################################
# 테스트
##########################################################################

from datetime import datetime

if __name__ == "__main__":

    today = datetime.today().strftime("%Y%m%d")

    weather = get_weather(
        destination="제주",
        target_date=today,
        base_date=today
    )

    print("최종 반환값")
    print(weather)