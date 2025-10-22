import os
import dotenv
from langchain_openai import ChatOpenAI

# API 연결 테스트
def test_connection():
    dotenv.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

    response = llm.invoke("Hello, say 'API connected!' in one sentence")
    print(response.content)

if __name__ == "__main__":
    test_connection()