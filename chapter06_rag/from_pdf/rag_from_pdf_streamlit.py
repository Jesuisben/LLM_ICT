from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# step01. PDF 로드
# =====================================================

loader = PyPDFLoader("../커피 매장 메뉴 및 이용 정보.pdf")
documents = loader.load()

print("\n==============================")
print("📄 PDF 로드 결과")
print("==============================")

print(f"총 문서 개수: {len(documents)}")

# 문서가 많으면 앞 10개만 출력
for idx, doc in enumerate(documents[:10]):
    print(f"\n[문서 {idx+1}]")
    print(doc.page_content[:200])   # 너무 길어서 앞 200글자만 출력

# =====================================================
# step02. 문서 분할
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunk = text_splitter.split_documents(documents)

print("\n==============================")
print("✂️ 문서 분할 결과")
print("==============================")

print(f"분할된 Chunk 개수: {len(chunk)}")

# 앞 10개만 출력
for idx, split in enumerate(chunk[:10]):
    print(f"\n[Chunk {idx+1}]")
    print(split.page_content[:200])

# =====================================================
# step03. 임베딩 + 벡터 DB 생성
# =====================================================

embed_object = OpenAIEmbeddings()

print("\n==============================")
print("🧠 임베딩 모델 생성 완료")
print("==============================")

print(embed_object)

vectorstore = Chroma.from_documents(
    documents=chunk,
    embedding=embed_object
)

print("\n==============================")
print("📦 Vector Store 생성 완료")
print("==============================")

print(vectorstore)

retriever = vectorstore.as_retriever()

print("\n==============================")
print("🔍 Retriever 생성 완료")
print("==============================")

print(retriever)

# =====================================================
# step04. Prompt Template
# =====================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "너는 카페 직원이야. 제공된 정보만 사용해서 질문에 답해줘."
    ),

    MessagesPlaceholder(variable_name="chat_history"),

    (
        "human",
        "카페 정보:\n{context}\n\n질문:\n{question}"
    )
])

print("\n==============================")
print("📝 Prompt Template")
print("==============================")

print(prompt)

# =====================================================
# step05. LLM 생성
# =====================================================

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=100
)

print("\n==============================")
print("🤖 LLM 모델 정보")
print("==============================")

print(model)

# =====================================================
# step06. 대화 기록 메모리
# =====================================================

chat_history = InMemoryChatMessageHistory()

print("\n==============================")
print("💬 초기 대화 기록")
print("==============================")

print(chat_history.messages)

# =====================================================
# step07. RAG Chain 구성
# =====================================================

rag_chain = (
    {
        "context": retriever,
        "question": lambda x: x,
        "chat_history": lambda x: chat_history.messages
    }
    | prompt
    | model
    | StrOutputParser()
)

print("\n==============================")
print("🔗 RAG Chain 생성 완료")
print("==============================")

print(rag_chain)

# =====================================================
# step08. 질문 실행
# =====================================================

question = "초코 케이크와 잘 어울리는 커피는 뭐야?"

print("\n==============================")
print("🙋 사용자 질문")
print("==============================")

print(question)

# Retriever 검색 결과 확인
retrieved_docs = retriever.invoke(question)

print("\n==============================")
print("📚 Retriever 검색 결과")
print("==============================")

print(f"검색된 문서 개수: {len(retrieved_docs)}")

# 앞 10개만 출력
for idx, doc in enumerate(retrieved_docs[:10]):
    print(f"\n[검색 문서 {idx+1}]")
    print(doc.page_content[:300])

# 최종 RAG 실행
answer = rag_chain.invoke(question)

# =====================================================
# step09. 대화 기록 저장
# =====================================================

chat_history.add_user_message(question)
chat_history.add_ai_message(answer)

print("\n==============================")
print("🤖 최종 답변")
print("==============================")

print(answer)

# =====================================================
# step10. 저장된 대화 기록 확인
# =====================================================

print("\n==============================")
print("🧠 저장된 대화 기록")
print("==============================")

messages = chat_history.messages

print(f"메시지 개수: {len(messages)}")

# 앞 10개만 출력
for idx, msg in enumerate(messages[:10]):
    print(f"\n[메시지 {idx+1}]")
    print(type(msg).__name__)
    print(msg.content)