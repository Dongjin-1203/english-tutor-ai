# 대화 기록 저장
# from langchain.memory import ConversationBufferMemory
from langchain_core.memory import ConversationBufferMemory
# 새 메모리 생성
def create_memory():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    return memory

# 대화 기록 가져오기
def get_chat_history(memory):
    history = memory.load_memory_variables({})
    return history["chat_history"]

# 대화 기록 초기화
def clear_memory(memory):
    memory.clear()