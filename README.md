# english-tutor-ai
---
## 개발 배경
나는 영어를 못한다. 하지만 나중에 해외에서 일해보고 싶은 큰 꿈이 있다. 그래서 여러 서적이나 강의를 보고 공부를 해보았지만 일정 수준 이상 올라가지 않았다. 다른 고득점자 후기를 보았을때, 대부분 고액 강의 같은 상급 노하우들을 통해 득점을 한 것을 심심치 않게 확인할 수 있었다. 돈이 없는 나는 고민을 하였고, 나는 LLM을 개발할 줄 안다는 것을 떠올렸고 실제 어떤 학습 업체들은 AI로 학습을 돕는다고 광고를 하는 것을 보았다. 

**나도 만들 수 있는데 돈을 굳이 왜써야하지?? 내가 만들어서 쓰면 일석이조인데...** 그래서 지난번 한영 번역 AI를 Seq2Seq 트랜스포머 모델로 만들었던 것을 발전시켜 LLM API를 활용해 학습에 도움을 줄 수 있는 AI 챗봇을 만들어 볼 계획이다.

일차적인 목표는 다음과 같다.
1. 문법 교정 + 설명
2. 자연스러운 표현 제안
3. 난이도별 예문 생성
4. 번역 + 뉘앙스 설명

추후 음성인식이 가능하도록 개발하고 추후 개인 학습 패턴 분석 및 맞춤형 학습 자료 추천까지 진행해볼 예정이다.

## 프로젝트 구조
```
english-tutor-ai/
├── .env                    # API 키 저장
├── requirements.txt        # 패키지 목록
├── main.py                # Streamlit 앱 (메인)
├── prompts/               # 프롬프트 템플릿들
│   ├── grammar.py
│   ├── translation.py
│   └── conversation.py
└── utils/                 # 유틸 함수들
    └── llm_handler.py     # LangChain 래퍼
```

## 환경 설정
랭체인을 이용할 예정이기 때문에 로컬에서 설치를 해야한다. 파이썬 버전은 3.11이다.
```
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install langchain langchain-openai streamlit python-dotenv
```
OpenAI API를 이용할 예정이기 때문에 `.env`파일에 API 키를 등록해준다.
```
# .env 파일 생성
OPENAI_API_KEY=your_api_key_here
```