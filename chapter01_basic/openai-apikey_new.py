# import os
# from dotenv import load_dotenv
#
# # 환경변수 가져오기 (기본값은 이 프로젝트, 폴더의 .env를 찾음)
# # 하지만 우리는 다른 폴더에 .env가 있으니까 그 경로를 지정해야함
# # 혹은 그 파일 자체를 시스템 환경변수로 등록해야함
# load_dotenv()
#
# # 시스템의 환경변수를 가져오는 방법
# # 가져오고 싶은 환경변수 이름 문자열로 넣기 (OPENAI_API_KEY)
# api_key = os.getenv("OPENAI_API_KEY")
# print(api_key)

# get_api_keys : 동시에 2개 이상의 key가 필요한 사이트에 사용
from utility.env_util import print_api_key, get_api_key, get_api_keys

find_api = "TEST_API_KEY"
# 환경변수 가져와서 출력하기
# hidden_size : 보여주고 싶은 문자열의 개수 설정
print_api_key(find_api, hidden_size=5)

# 환경변수 가져와서 변수에 넣기
api_key = get_api_key(find_api)
print(f"{find_api} : {api_key}")

keys_tuple = (
    find_api,
    "AMADEUS_CLIENT_ID",
    "MADONNA_KEY"
)

keys_dict = get_api_keys(keys_tuple)

for key in keys_dict:
    print(f"{key} : {keys_dict[key]}")