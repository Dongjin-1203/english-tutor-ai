# Streamlit App
import streamlit as st
from utils.llm_handler import run_chain
from prompts.grammar import GRAMMAR_SYSTEM_PROMPT
import dotenv

def main():

    # 환경변수 로드
    dotenv.load_dotenv()

    # UI 구성
    st.title("🎓 영어 문법 교정 AI")
    st.write("문장을 입력하면 문법을 교정해드립니다!")

    # 입력창
    user_text = st.text_area(
        "영어 문장 입력:",
        placeholder="예: I goes to school yesterday.",
        height=150
    )

    # 버튼
    if st.button("교정하기", type="primary"):
        if user_text.strip() == "":
            st.warning("문장을 입력해주세요!")
        else:
            with st.spinner("교정 중... 잠시만 기다려주세요."):
                # 프롬프트 실행
                corrected_text = run_chain(
                    GRAMMAR_SYSTEM_PROMPT,
                    user_text
                )
            st.success("교정 완료!")
            st.subheader("교정된 문장:")
            st.write(corrected_text)

if __name__ == "__main__":
    st.set_page_config(page_title="English Tutor AI", page_icon="🎓")
    main()