# =====================================================================
# Open AI LLM을 위한 utility module
# =====================================================================
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
# =====================================================================
# Chat Open AI 모델을 생성하는 함수
# =====================================================================
def create_model(
    model_name: str = 'gpt-4o-mini',
    temp: float = 0,
    model_key: str = ''
):
    print('create_model 생성 직전')
    print(model_key)
    mymodel = ChatOpenAI(model=model_name, temperature=temp, api_key=model_key)

    return mymodel
# =====================================================================
# YouTube 요약 관련 Chain을 생성하는 함수
# =====================================================================
def create_chain(model):
    prompt = ChatPromptTemplate.from_messages([(
            "system",
            """
다음 유튜브 영상 내용을 분석하여 아래 항목을 Markdown 형식으로 정리하세요.

### 핵심 주제
- ...

### 긍정/부정 분위기
- ...

### 주요 키워드
- ...

### 자주 언급된 인물
- ...

### 핵심 쟁점
- ...

영상 내용:

{context}
"""
    )])
    # create_stuff_documents_chain()은 LangChain에서 여러 개의 문서를 하나로 합쳐(Stuff) LLM에게 전달하는 체인을 생성하는 함수
    return create_stuff_documents_chain(model, prompt)
# =====================================================================
# 모든 영상들을 요약해주는 함수
# =====================================================================
def summarize_all_videos(chain, videos):
    for video in videos:
        documents = video.get('content')

        print('=' * 50)
        print(f'제목 : {video["title"]}')

        if documents:
            print('Documents :', documents)
            print(f'Document 개수 : {len(documents)}')

            video['summary'] = summarize_video(chain, docs=documents)

            print(video['summary'])

        else :
            print("문서가 없습니다.")
            continue
    # end for

    return videos
# =====================================================================
# 영상 1개를 요약해주는 함수
# =====================================================================
def summarize_video(chain, docs):
    if not docs:
        return '자막이 존재하지 않습니다.'

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents=docs)

    # chunks = chunks[:5] # 청크 수가 너무 크면 이 문장 주석 해제해 주세요.

    return chain.invoke({
        'context': chunks
    })
# ===== End Of File ======================================================