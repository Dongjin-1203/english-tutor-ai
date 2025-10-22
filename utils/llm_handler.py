# LangChain 관련 코드
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM 인스턴스 생성
def get_llm(temperature=0.3):
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("🚨 OPENAI_API_KEY가 설정되지 않았습니다!")
        st.info("Streamlit Cloud: Settings > Secrets에서 API 키를 설정하세요.")
        st.stop()
    
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        openai_api_key=api_key
    )

def run_chain(system_prompt, user_input, temperature=0.3):
    # 1. 프롬프트 구성
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{text}")
    ])
    
    # 2. 체인 구성
    chain = prompt | get_llm(temperature) | StrOutputParser()
    
    # 3. 실행
    result = chain.invoke({"text": user_input})
    return result

def run_chain_with_memory(system_prompt, user_input, memory, temperature=0.3):
    """Memory를 사용하는 체인 (session_state 방식)"""
    from utils.memory_handler import format_history_for_prompt
    
    # 1. 대화 기록을 텍스트로 변환
    history_text = format_history_for_prompt(memory)
    
    # 2. 프롬프트에 히스토리 포함
    full_prompt = system_prompt + history_text
    
    # 3. 프롬프트 템플릿 생성
    prompt = ChatPromptTemplate.from_messages([
        ("system", full_prompt),
        ("user", "{text}")
    ])
    
    # 4. 체인 구성 및 실행
    chain = prompt | get_llm(temperature) | StrOutputParser()
    result = chain.invoke({"text": user_input})
    
    return result