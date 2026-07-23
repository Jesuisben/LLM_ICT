from utility.env_util import get_api_key, print_api_key, get_api_keys

print_api_key("TEST_API_KEY", hidden_size=5)

print('\n# 하나의 Key 정보를 확인합니다.')
find_api = "TEST_API_KEY"
api_key = get_api_key(find_api)
print(f'{find_api} : [{api_key}]')

print('\n# 여러 개의 Key 정보를 확인합니다.')
keys_tuple = (
    "AMADEUS_CLIENT_ID",
    "MADONNA_KEY",
    "TEST_API_KEY"
)

keys_dict = get_api_keys(
    keys_tuple
)

for key in keys_tuple:
    print(f'{key} : {keys_dict[key]}')