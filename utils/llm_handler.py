# LangChain 관련 코드
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM 인스턴스 생성
def get_llm(tamperature=0.3):
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=tamperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# 프롬프트 실행
def run_chain(system_promt, user_input):
    # 1. 프롬프트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_promt),
        ("user", "{text}")
    ])

    # 2. 체인 구성(핵심)
    chain = prompt| get_llm() | StrOutputParser()

    # 3. 실행
    result = chain.invoke({"text": user_input})

    return result