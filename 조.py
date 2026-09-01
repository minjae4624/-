import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="귀멸의 칼날: 혈풍담 Style",
    page_icon="⚔️",
    layout="wide"
)

# 혈풍담 테마 커스텀 CSS 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=East+Sea+Dokdo&family=Noto+Serif+KR:wght@600;900&display=swap');

    /* 메인 배경 및 기본 폰트 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0c 0%, #1a0505 50%, #050000 100%);
        color: #e6e6e6;
        font-family: 'Noto Serif KR', serif;
    }

    /* 타이틀 디자인 */
    .title-text {
        font-family: 'East Sea Dokdo', cursive;
        font-size: 4.5rem !important;
        color: #ff3333;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #800000;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .subtitle-text {
        text-align: center;
        color: #cccccc;
        font-size: 1.2rem;
        letter-spacing: 3px;
        margin-bottom: 30px;
    }

    /* 혈풍담 스타일 카드 UI */
    .card {
        background: rgba(20, 20, 25, 0.85);
        border: 2px solid #331111;
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    .card:hover {
        border-color: #ff3333;
        box-shadow: 0 0 25px rgba(255, 50, 50, 0.4);
        transform: translateY(-2px);
    }

    /* 커스텀 버튼 (화염/혈귀술 스타일) */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4a0000 0%, #800000 50%, #4a0000 100%);
        color: #ffffff !important;
        font-family: 'Noto Serif KR', serif;
        font-weight: 900;
        font-size: 1.1rem;
        border: 1px solid #ff4d4d;
        border-radius: 2px;
        padding: 12px 24px;
        text-shadow: 0 0 5px #000;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #990000 0%, #ff1a1a 50%, #990000 100%);
        box-shadow: 0 0 15px #ff3333;
        border-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown('<p class="title-text">鬼滅の刃 : 血風譚</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">[ 귀멸의 칼날 : 히노카미 혈풍담 UI ]</p>', unsafe_allow_html=True)

st.divider()

# 메인 콘텐츠 구성
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="card">
        <h3 style="color: #ff4d4d; border-bottom: 1px solid #4a0000; padding-bottom: 8px;">⚔️ 대전 모드</h3>
        <p style="color: #bbb;">버전 선택 및 대전 모드를 실행합니다. 원하는 대원과 혈귀를 선택해 대결하세요.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("대전 시작하기"):
        st.error("불꽃의 호흡 제1형 — 시라누이!")

with col2:
    st.markdown("""
    <div class="card">
        <h3 style="color: #4da6ff; border-bottom: 1px solid #002b50; padding-bottom: 8px;">📜 솔로 플레이 (솔로 단편)</h3>
        <p style="color: #bbb;">탄지로의 여정을 추체험하는 스토리 모드입니다. 무한열차 편까지의 이야기를 확인하세요.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("스토리 기록 보기"):
        st.info("물의 호흡 제10형 — 생생전변!")
