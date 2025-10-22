# LangChain 관련 코드
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
    # 1. 메모리에서 대화 기록 가져오기
    chat_history = memory.load_memory_variables({})
    
    # 2. 프롬프트 구성 (MessagesPlaceholder 사용!)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),  # ✅ 이렇게 수정!
        ("user", "{input}")
    ])
    
    # 3. 체인 구성
    chain = prompt | get_llm(temperature) | StrOutputParser()
    
    # 4. 실행 (chat_history 전달)
    result = chain.invoke({
        "input": user_input,
        "chat_history": chat_history.get("history", [])
    })
    
    # 5. 메모리에 대화 저장
    memory.save_context(
        {"input": user_input},
        {"output": result}
    )
    
    return result