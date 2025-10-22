# 대화 기록 저장
from langchain.memory import ConversationBufferMemory

"""Memory 관리 함수들 (session_state 사용)"""

def create_memory():
    """메모리 초기화 - 빈 리스트 반환"""
    return []

def get_chat_history(memory):
    """대화 기록 가져오기"""
    return memory

def add_to_memory(memory, user_input, ai_response):
    """대화 기록 추가"""
    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": ai_response})
    return memory

def clear_memory(memory):
    """대화 기록 초기화"""
    memory.clear()
    return memory

def format_history_for_prompt(memory):
    """프롬프트용 히스토리 포맷팅"""
    if not memory:
        return ""
    
    formatted = "\n\nPrevious conversation:\n"
    for msg in memory:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted += f"{role}: {msg['content']}\n"
    
    return formatted