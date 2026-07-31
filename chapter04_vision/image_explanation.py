#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 인터넷 이미지 설명 요청
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": "1~2 개의 짧은 답변을 제시해줘"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해 간략히 설명해 주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://images.unsplash.com/photo-1736264335247-8ec5664c8328?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=50,
    temperature=0.2
)

print('response')
print(response)

print('\nresponse.choices[0].message.content')
print(response.choices[0].message.content)


# In[2]:


# 로컬 파일 실습시 이미지 사이즈가 너무 크면 다음과 같은 메시지가 나올수 있습니다.
# 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_image_url'}}
# 이런 경우 '비율 고정하면서 리사이즈' 작업을 하도록 합니다.
# 첨부 파일 : image_resize.py

# 로컬 이미지 설명 요청
import base64

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 양양 스카이워크 지브리 이미지
image_path = "../images/yangyang_skywalk_512.png"
# image_path = "../images/yangyang_skywalk.png"

# 이미지를 base64로 인코딩
base64_image = encode_image(image_path)

# print(base64_image)
print(base64_image[:100]) # 너무 길어서 앞 100글자만 출력


# In[3]:


messages = [
    {
        "role": "system",
        "content": "1~2 개의 짧은 답변을 제시해줘"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해 간략히 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=50,
    temperature=0.2
)

response.choices[0].message.content


# In[4]:


# 이미지 비교해보기
compare_image_base64_01 = encode_image("../images/image_compare_01.png")
compare_image_base64_02 = encode_image("../images/image_compare_02.png")

messages = [
    {
        "role": "system",
        "content": "1~2 개의 짧은 답변을 제시해줘"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "이미지의 차이점을 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{compare_image_base64_01}",
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{compare_image_base64_02}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=50,
    temperature=0.2
)

response.choices[0].message.content


# In[5]:


# 그래프 이미지 비교해보기
cafe_sales_2025_base64 = encode_image("../images/cafe_sales_2025.png")
cafe_sales_2026_base64 = encode_image("../images/cafe_sales_2026.png")

messages = [
    {
        "role": "system",
        "content": "1~2 개의 짧은 답변을 제시해줘"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "2025/2026년 데이터에 어떤 변화가 있는지 짧게 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{cafe_sales_2025_base64}",
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{cafe_sales_2026_base64}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=100,
    temperature=0.2
)

response.choices[0].message.content





