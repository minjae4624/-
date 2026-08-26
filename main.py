import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="✨ MBTI 진로 탐험 대모험! 🚀",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 화려한 커스텀 CSS 스타일링
st.markdown("""
<style>
    /* 전체 배경 그래디언트 및 폰트 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #FFFFFF;
    }
    
    /* 사이드바 스타일링 */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }

    /* 메인 타이틀 카리스마 효과 */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#FFD700, #FF69B4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 0px;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.3rem;
        color: #E0E0E0;
        margin-bottom: 2rem;
    }

    /* 직업 추천 카드 스타일링 */
    .job-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    /* 강조 텍스트 및 배지 */
    .badge {
        background-color: #FF477E;
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .mbti-tag {
        font-size: 2.5rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
    }
</style>
""", unsafe_allow_allow_html=True)

# 3. MBTI 데이터베이스 (이모지, 설명, 추천 직업, 핵심 역량)
mbti_data = {
    "INTJ": {
        "title": "🦉 용의주도한 전략가 (Mastermind)",
        "desc": "상상력이 풍부하며 철저한 계획을 세우는 전략가 형이에요! 🧠⚡",
        "jobs": [
            {"name": "🤖 AI 데이터 과학자", "desc": "복잡한 데이터를 분석하고 미래를 예측하는 모델을 만들어요!"},
            {"name": "💼 경영 컨설턴트", "desc": "기업의 문제점을 진단하고 스마트한 해결책을 제시합니다."},
            {"name": "🚀 우주항공 공학자", "desc": "새로운 우주선을 설계하고 미지의 세계를 탐험해요."}
        ],
        "skills": "🎯 비판적 사고 | 📐 전략적 계획 | 💡 문제 해결"
    },
    "INTP": {
        "title": "🧪 아이디어 파이프라인 논리술사 (Thinker)",
        "desc": "끊임없이 호기심을 가지며 원리를 탐구하는 지적 호기심 왕! 🔬📚",
        "jobs": [
            {"name": "💻 시스템 아키텍트", "desc": "소프트웨어의 거대한 구조를 다듬고 설계합니다."},
            {"name": "🧬 바이오 연구원", "desc": "생명 현상의 비밀을 밝혀내고 치료제를 연구해요."},
            {"name": "🌌 이론 물리학자", "desc": "우주의 법칙과 자연계의 비밀을 방정식으로 풀어냅니다."}
        ],
        "skills": "🔍 원리 탐구 | 🧩 논리 분석 | 💡 창의적 발상"
    },
    "ENTJ": {
        "title": "👑 대담한 통솔자 (Commander)",
        "desc": "대담하고 집요하며 비전을 향해 리드하는 리더 타입! 🎯🔥",
        "jobs": [
            {"name": "🦄 스타트업 대표(CEO)", "desc": "혁신적인 아이디어로 세상을 바꾸는 회사를 이끌어요."},
            {"name": "🏛️ 정치·행정가", "desc": "더 나은 사회를 만들기 위한 정책과 비전을 제시합니다."},
            {"name": "📈 투자은행가(IB)", "desc": "거대한 자금을 운용하고 대형 프로젝트를 성공시킵니다."}
        ],
        "skills": "👑 리더십 | 📢 설득 및 추진력 | 🗺️ 비전 제시"
    },
    "ENTP": {
        "title": "⚡ 뜨거운 열정의 변론가 (Debater)",
        "desc": "새로운 관점을 제시하고 솔직한 논쟁을 즐기는 아이디어 아이콘! 💡💥",
        "jobs": [
            {"name": "🎨 크리에이티브 디렉터", "desc": "세상을 놀라게 할 파격적인 마케팅 아이디어를 기획해요."},
            {"name": "⚖️ 변호사", "desc": "날카로운 논리로 클라이언트를 변호하고 정의를 실현해요."},
            {"name": "🎮 게임 기획자", "desc": "세상에 없던 새로운 규칙의 재미있는 게임을 설계합니다."}
        ],
        "skills": "🗣️ 변론·설득 | 🌟 융합 사고 | 🚀 혁신성"
    },
    "INFJ": {
        "title": "🔮 통찰력 있는 예언자 (Advocate)",
        "desc": "조용하지만 세상을 바꾸는 따뜻한 비전을 품은 사람! 🌟🕊️",
        "jobs": [
            {"name": "🧠 심리치료사", "desc": "사람들의 깊은 마음의 상처를 보듬고 치유를 도와요."},
            {"name": "✍️ 웹툰 작가 / 소설가", "desc": "깊은 감동과 메시지를 담은 스토리로 세상을 울립니다."},
            {"name": "🌍 NGO 활동가", "desc": "인류와 환경을 위한 가치 있는 변화를 만들어갑니다."}
        ],
        "skills": "❤️ 공감 능력 | 👁️ 깊은 통찰 | 📜 가치 중심"
    },
    "INFP": {
        "title": "🎨 이상적인 중재자 (Healer)",
        "desc": "성실하고 신중하며 예술적 감수성이 풍부한 낭만파! 🌈✨",
        "jobs": [
            {"name": "🎬 영화 감독", "desc": "자신만의 독창적인 세계관과 예술적 감성을 영상에 담아요."},
            {"name": "🎵 음악 프로듀서", "desc": "사람들의 영혼을 울리는 아름다운 멜로디를 만듭니다."},
            {"name": "🌿 환경 콘텐츠 크리에이터", "desc": "지구를 지키는 감성적인 스토리를 전달합니다."}
        ],
        "skills": "🎨 예술적 감수성 | 🕊️ 진정성 | ✍️ 창의적 표현"
    },
    "ENFJ": {
        "title": "🌟 정의로운 선도자 (Protagonist)",
        "desc": "선한 영향력으로 사람들을 고취시키고 이끄는 영웅! 💖📢",
        "jobs": [
            {"name": "👩‍🏫 진로진학 교사", "desc": "학생들의 잠재력을 발견하고 꿈을 향해 나아가게 돕습니다."},
            {"name": "🤝 HRD(인재개발) 전문가", "desc": "기업 구성원들의 성장을 지원하고 팀을 이끌어요."},
            {"name": "🎙️ 아나운서 / MC", "desc": "밝고 긍정적인 에너지로 대중과 소통합니다."}
        ],
        "skills": "🤝 코칭·임파워링 | 🗣️ 동기부여 | 💗 인간관계"
    },
    "ENFP": {
        "title": "🦄 재기발랄한 활동가 (Campaigner)",
        "desc": "에너지가 넘치고 언제나 자유로운 영혼의 소유자! 🎈🎉",
        "jobs": [
            {"name": "📹 유튜버 / 인플루언서", "desc": "자신의 일상과 통통 튀는 아이디어로 세상에 즐거움을 줘요."},
            {"name": "🎪 이벤트 기획자", "desc": "사람들을 신나게 만드는 대형 축제와 페스티벌을 만듭니다."},
            {"name": "🎨 UX/UI 디자이너", "desc": "사용자가 즐겁고 편리하게 쓸 수 있는 앱 화면을 그려요."}
        ],
        "skills": "⚡ 넘치는 에너지 | 🎨 친화력 | 💡 즉흥적 창의성"
    },
    "ISTJ": {
        "title": "🛡️ 청렴결백한 논리주의자 (Inspector)",
        "desc": "사실에 기반하여 신중하고 확실하게 임무를 완수하는 파수꾼! 📐🔒",
        "jobs": [
            {"name": "📊 공인회계사(CPA)", "desc": "투명하고 정확하게 재무 상태를 분석하고 관리해요."},
            {"name": "🛡️ 정보보안 전문가", "desc": "해킹으로부터 중요한 데이터와 시스템을 철통 방어합니다."},
            {"name": "⚖️ 법원 행정관", "desc": "원칙과 규정에 따라 공정하게 법적 절차를 집행합니다."}
        ],
        "skills": "📊 정확성 | 🏛️ 원칙 준수 | 🔍 세심함"
    },
    "ISFJ": {
        "title": "💖 용감한 수호자 (Protector)",
        "desc": "소중한 사람들을 온화하고 헌신적으로 지키는 든든한 조력자! 🌸🛡️",
        "jobs": [
            {"name": "🩺 소아과 의사 / 간호사", "desc": "환자들의 따뜻한 건강 수호자가 되어 치료합니다."},
            {"name": "🏫 초등학교 교사", "desc": "아이들의 눈높이에서 따뜻한 보살핌과 배움을 줍니다."},
            {"name": "🏛️ 박물관 큐레이터", "desc": "소중한 문화유산을 보존하고 대중에게 알립니다."}
        ],
        "skills": "🌸 배려와 봉사 | 📝 섬세한 관리 | 🤝 헌신성"
    },
    "ESTJ": {
        "title": "💼 엄격한 관리자 (Executive)",
        "desc": "사물과 사람을 관리하는 데 타의 추종을 불허하는 조직의 리더! 🏢📋",
        "jobs": [
            {"name": "🏗️ 건설 프로젝트 매니저", "desc": "거대한 건축 현장의 모든 공정과 인력을 총괄해요."},
            {"name": "👮 경찰 간부", "desc": "질서와 법을 유지하며 시민들의 안전을 책임집니다."},
            {"name": "🏬 총괄 운영 디렉터(COO)", "desc": "회사의 전체적인 체계와 효율성을 극대화합니다."}
        ],
        "skills": "📋 조직 관리 | ⏱️ 시간·자원 효율화 | 🎯 목표 달성"
    },
    "ESFJ": {
        "title": "🤝 사교적인 외교관 (Provider)",
        "desc": "타인을 돕는 것에 열정적인 인기쟁이 사교가! 🍰🎁",
        "jobs": [
            {"name": "✈️ 승무원", "desc": "최고의 서비스와 미소로 승객들의 안전한 여행을 도와요."},
            {"name": "🏨 호텔 지배인", "desc": "고객에게 잊지 못할 특별한 경험과 휴식을 선물합니다."},
            {"name": "🏥 사회복지사", "desc": "도움이 필요한 이웃들에게 실질적인 복지 혜택을 연결해요."}
        ],
        "skills": "🤝 뛰어난 친화력 | 🎁 타인 케어 | 🗣️ 원활한 소통"
    },
    "ISTP": {
        "title": "🛠️ 만능 재주꾼 (Craftsman)",
        "desc": "도구를 자유자재로 다루는 냉철한 이성주의자! ⚙️🏍️",
        "jobs": [
            {"name": "🏎️ 카레이서 / 튜너", "desc": "스피드를 즐기며 최고의 기계 성능을 이끌어냅니다."},
            {"name": "🛰️ 드론 제어 전문가", "desc": "최첨단 드론을 조종하고 최적의 비행 경로를 설정해요."},
            {"name": "🔍 법의학 수사관", "desc": "현장의 증거들을 기술적으로 분석하여 진실을 밝힙니다."}
        ],
        "skills": "🛠️ 기계·도구 숙련 | ❄️ 침착함 | 🎯 현장 대응력"
    },
    "ISFP": {
        "title": "🎨 호기심 많은 예술가 (Artist)",
        "desc": "새로운 것을 탐험하고 예술적 감각이 뛰어난 감성파! 🌻📸",
        "jobs": [
            {"name": "📸 패션 사진작가", "desc": "찰나의 아름다움을 카메라 프레임에 완벽히 담아냅니다."},
            {"name": "💄 메이크업 아티스트", "desc": "얼굴이라는 도화지에 개성 있는 아름다움을 표현해요."},
            {"name": "🐾 동물 행동 교정사", "desc": "말하지 못하는 동물의 마음을 이해하고 치유합니다."}
        ],
        "skills": "📸 시각적 감각 | 🌸 온화함 | 🎨 미적 감수성"
    },
    "ESTP": {
        "title": "🔥 수완좋은 탐험가 (Dynamo)",
        "desc": "위험을 두려워하지 않고 직관적으로 문제를 해결하는 스릴러! 🏄‍♂️⚡",
        "jobs": [
            {"name": "🎬 스턴트 연기자", "desc": "온몸을 던져 화려하고 박진감 넘치는 액션을 연출합니다."},
            {"name": "📊 펀드매니저 / 트레이더", "desc": "빠르게 변하는 금융 시장에서 과감한 결단으로 수익을 냅니다."},
            {"name": "🚒 소방관 / 구급대원", "desc": "위급한 현장에 가장 먼저 뛰어들어 인명을 구합니다."}
        ],
        "skills": "⚡ 순발력 | 🔥 담력 | 🎯 즉각적 행동력"
    },
    "ESFP": {
        "title": "🎉 자유로운 연예인 (Performer)",
        "desc": "주위 사람을 지루할 틈이 없게 만드는 분위기 메이커! 🎤🌟",
        "jobs": [
            {"name": "🎭 뮤지컬 배우", "desc": "무대 위에서 노래와 연기로 관객들에게 감동과 전율을 줍니다."},
            {"name": "🛍️ 쇼호스트", "desc": "재치 있는 입담으로 상품의 매력을 폭발적으로 전달해요."},
            {"name": "💃 댄스 안무가", "desc": "신나는 리듬에 맞춰 독창적인 댄스 동작을 창작합니다."}
        ],
        "skills": "🎤 표현력 | 🎉 유쾌한 에너제틱 | 🌟 무대 체질"
    }
}

# 4. 헤더 영역
st.markdown("<h1 class='main-title'>✨ 🎉 MBTI 진로 탐험 대모험! 🎉 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>나의 MBTI를 선택하고, 나에게 꼭 맞는 '인생 직업'을 찾아보세요! 🚀🎨</p>", unsafe_allow_html=True)

# 5. 사이드바 - MBTI 선택 및 탐색
st.sidebar.markdown("## 🧭 MBTI 탐색기")
st.sidebar.write("당신의 4글자 MBTI를 선택하세요! 🔮")

category = st.sidebar.radio(
    "MBTI 그룹 선택 📂",
    ["분석형 (NT)", "외교형 (NF)", "관리형 (SJ)", "탐험가형 (SP)"]
)

if category == "분석형 (NT)":
    selected_mbti = st.sidebar.selectbox("MBTI 선택 👇", ["INTJ", "INTP", "ENTJ", "ENTP"])
elif category == "외교형 (NF)":
    selected_mbti = st.sidebar.selectbox("MBTI 선택 👇", ["INFJ", "INFP", "ENFJ", "ENFP"])
elif category == "관리형 (SJ)":
    selected_mbti = st.sidebar.selectbox("MBTI 선택 👇", ["ISTJ", "ISFJ", "ESTJ", "ESFJ"])
else:
    selected_mbti = st.sidebar.selectbox("MBTI 선택 👇", ["ISTP", "ISFP", "ESTP", "ESFP"])

# 재미있는 풍선 효과
if st.sidebar.button("🎈 축하 효과 터뜨리기!"):
    st.balloons()

# 6. 메인 화면 - 선택된 MBTI 결과 출력
info = mbti_data[selected_mbti]

st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"<div class='mbti-tag'>{selected_mbti}</div>", unsafe_allow_html=True)
    st.markdown(f"### {info['title']}")
    st.write(info['desc'])
    st.info(f"**⚡ 핵심 강점 키워드**\n\n{info['skills']}")

with col2:
    st.markdown("### 🌟 추천 대표 직업 TOP 3")
    for idx, job in enumerate(info['jobs'], 1):
        st.markdown(f"""
        <div class='job-card'>
            <h4><span class='badge'>Best {idx}</span> {job['name']}</h4>
            <p style='font-size: 1.05rem; margin-top: 10px;'>{job['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# 7. 하단 인터랙티브 확장 가이드
st.markdown("---")
st.markdown("### 🎁 진로 성장을 위한 특별 꿀팁 코너!")

with st.expander("🎓 이 직업을 갖기 위해 지금 무엇을 준비해야 할까요?"):
    st.write(f"""
    * **{selected_mbti}** 유형은 자신의 강점인 **'{info['skills'].split('|')[0].strip()}'** 능력을 살릴 때 가장 몰입합니다!
    * 관찰일기 쓰기, 관련 동아리 활동, 온라인 강좌 수강 등 작지만 꾸준한 프로젝트를 시작해 보세요! 🚀
    * 당신의 성향을 이해하고 강점을 다듬는다면 어떤 분야에서든 빛나는 리더가 될 수 있습니다! 💎
    """)

# 하단 푸터
st.write("\n\n")
st.markdown("<p style='text-align: center; color: #BBB;'>Made with ❤️ for Future Leaders | Streamlit Career Edu WebApp 🌈</p>", unsafe_allow_html=True)
