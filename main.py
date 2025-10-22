# Streamlit App
import streamlit as st
from utils.llm_handler import run_chain
from prompts.grammar import GRAMMAR_SYSTEM_PROMPT
from prompts.translate import TRANSLATION_SYSTEM_PROMPT
from prompts.conversation import get_conversation_prompt
import dotenv

def main():

    # 환경변수 로드
    dotenv.load_dotenv()

    # ✅ session_state 초기화 (이 부분 추가!)
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    
    if "conv_messages" not in st.session_state:
        st.session_state.conv_messages = []

    # ✅ 추가
    if "current_scenario" not in st.session_state:
        st.session_state.current_scenario = "카페"
    
    if "current_level" not in st.session_state:
        st.session_state.current_level = "intermediate"

    # UI 구성
    st.title("🎓 영어 문법 교정 AI")

    # 탭 구조로 변경
    tab1, tab2, tab3 = st.tabs(["문법 교정", "번역", "회화 연습"])

    # 문법 교정
    with tab1:
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

    # 번역
    with tab2:
        st.write("한국어를 자연스러운 영어로 번역합니다!")

        korean_text = st.text_area(
            "한국어 문장 입력:",
            placeholder="예: 안녕하세요, 오늘 기분이 어떠세요?",
            height=150
        )
        if st.button("번역하기", type="primary", key="translate"):
            if korean_text.strip() == "":
                st.warning("문장을 입력해주세요!")
            else:
                with st.spinner("번역 중... 잠시만 기다려주세요."):
                    translation_result = run_chain(
                        TRANSLATION_SYSTEM_PROMPT,
                        korean_text
                    )
                st.success("번역 완료!")
                st.subheader("번역 결과:")
                st.write(translation_result)

    # 회화 연습
    with tab3:
        st.write("AI와 영어 대화를 연습하세요!")

        # 시나리오 선택
        scenario = st.selectbox(
            "상황 선택:",
            ["카페", "공항", "면접", "쇼핑", "병원"]
        )

        # 난이도 선택
        level = st.radio(
            "난이도:",
            ["beginner", "intermediate", "advanced"],
            horizontal=True
        )

        # 대화 시작 버튼
        if st.button("대화 시작"):
            st.session_state.conversation_started = True
            st.session_state.messages = []
            
            # ✅ scenario와 level을 session_state에 저장
            st.session_state.current_scenario = scenario
            st.session_state.current_level = level
            
            # AI 첫 멘트
            prompt = get_conversation_prompt(scenario, level)
            first_message = run_chain(prompt, "Start the conversation")
            st.session_state.messages.append({"role": "ai", "content": first_message})
            st.rerun()

        # 대화 기록 표시
        if st.session_state.conversation_started == True:
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]
                
                if role == "user":
                    with st.chat_message("user", avatar="🧑"):
                        st.write(content)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(content)

            # 사용자 입력
            user_input = st.text_input("당신의 응답 (영어로):")
            
            if st.button("보내기"):
                # ✅ session_state에서 가져와서 다시 생성
                prompt = get_conversation_prompt(
                    st.session_state.current_scenario, 
                    st.session_state.current_level
                )
                
                response = run_chain(prompt, user_input)
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "ai", "content": response})
                st.rerun()
            
if __name__ == "__main__":
    st.set_page_config(page_title="English Tutor AI", page_icon="🎓")
    main()