import streamlit as st
import random
import time

# 1. 페이지 및 테마 설정
st.set_page_config(page_title="귀멸의 칼날: 혈풍담", page_icon="⚔️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=East+Sea+Dokdo&family=Noto+Serif+KR:wght@600;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0a0c 0%, #1a0505 50%, #050000 100%);
        color: #e6e6e6;
        font-family: 'Noto Serif KR', serif;
    }
    .title-text {
        font-family: 'East Sea Dokdo', cursive;
        font-size: 4rem !important;
        color: #ff3333;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #800000;
        text-align: center;
        margin-bottom: 0px;
    }
    .battle-card {
        background: rgba(20, 20, 25, 0.9);
        border: 2px solid #551111;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.2);
        text-align: center;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4a0000 0%, #800000 50%, #4a0000 100%);
        color: #ffffff !important;
        font-weight: 900;
        border: 1px solid #ff4d4d;
        padding: 10px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #990000 0%, #ff1a1a 50%, #990000 100%);
        box-shadow: 0 0 15px #ff3333;
    }
</style>
""", unsafe_allow_html=True)

# 2. 게임 데이터 정의
CHARACTERS = {
    "카마도 탄지로": {"hp": 100, "atk": 18, "skill": "히노카미 카구라", "skill_damage": 35, "color": "#ff4d4d"},
    "렌고쿠 쿄주로": {"hp": 110, "atk": 22, "skill": "화염의 호흡 제9형 연옥", "skill_damage": 42, "color": "#ff8c00"},
    "토미오카 기유": {"hp": 105, "atk": 17, "skill": "물의 호흡 제11형 잔잔함", "skill_damage": 30, "color": "#1e90ff"},
    "아카자": {"hp": 120, "atk": 20, "skill": "파괴살 멸식", "skill_damage": 38, "color": "#ff007f"},
    "루이": {"hp": 95, "atk": 16, "skill": "각실뢰", "skill_damage": 32, "color": "#ffffff"}
}

# 3. 게임 상태 초기화 (Session State)
if "game_state" not in st.session_state:
    st.session_state.game_state = "SELECT"  # SELECT, BATTLE, END
if "p1" not in st.session_state:
    st.session_state.p1 = None
if "p2" not in st.session_state:
    st.session_state.p2 = None
if "logs" not in st.session_state:
    st.session_state.logs = []

# 4. 헤더
st.markdown('<p class="title-text
