# ============================================================
# OpenAI Client 생성 모듈
# ============================================================
import os

from openai import OpenAI
# ============================================================
# Project Root
# ============================================================
# PROJECT_ROOT = Path(__file__).resolve().parents[2]
#
# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0,str(PROJECT_ROOT))

from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)
# ============================================================
# OpenAI Client 객체를 생성하여 반환해주는 함수
# ============================================================
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY가 설정되어 있지 않습니다.\n"
            ".env 파일을 확인하세요."
        )

    return OpenAI(api_key=api_key)
# ============================================================