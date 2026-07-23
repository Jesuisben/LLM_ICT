import os

from pathlib import Path
from dotenv import load_dotenv

# .env 파일의 위치
ENV_FILE_PATH = Path(__file__).resolve().parent.parent.parent / "myenv" / ".env"

# 프로그램 시작 시 .env 파일 내용을 한번 로딩하여 환경 변수로 등록
# load_dotenv() # 현재 프로젝트에 있는 경우
load_dotenv(ENV_FILE_PATH)

def get_api_key(key_name: str) -> str | None:
    """
    환경 변수 값을 반환한다.
    없으면 None을 반환한다.
    """
    api_key = os.getenv(key_name)

    if api_key is None:
        print(f"\n환경 변수 '{key_name}'를 찾을 수 없습니다.")
        return None

    return api_key


# hidden_size = 50 # 보안을 위해 API Key의 뒤쪽을 *로 가리기 위한 숫자입니다.
# OpenAI API Key를 일부는 그대로 출력하고, 나머지는 *로 가리는(masking) 역할을 합니다.
def print_api_key(key_name: str = "OPENAI_API_KEY", hidden_size: int = 50):
    """API Key를 일부만 출력"""
    api_key = os.getenv(key_name)

    if not api_key:
        print(f"\n{key_name}를 찾을 수 없습니다.")
        return

    print(f"\nAPI Key를 일부만 출력")
    hidden_size = min(hidden_size, len(api_key))
    print(f"{key_name} : [{api_key[:-hidden_size]}{'*' * hidden_size}]")


def get_api_keys(key_names: tuple[str, ...]) -> dict[str, str | None]:
    """
    여러 개의 환경 변수를 한 번에 반환한다.

    Parameters
    ----------
    key_names : tuple[str, ...]
        환경 변수 이름들의 튜플

    Returns
    -------
    dict[str, str | None]
    """
    result = {}

    for key_name in key_names:
        api_key = os.getenv(key_name)

        if api_key is None:
            print(f"환경 변수 '{key_name}'를 찾을 수 없습니다.")

        result[key_name] = api_key

    return result

if __name__ == "__main__":
    print(f".env 파일의 위치 : {ENV_FILE_PATH}")

'''
일반 파일에서 다음과 같이 간단히 사용할 수 있습니다.
from utility.env_util import get_api_key

find_api = "OPENAI_API_KEY"
api_key = get_api_key(find_api)

client = OpenAI(api_key=api_key)
'''