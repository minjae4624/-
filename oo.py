import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="VALORANT Map & Agent Pick Rates",
    page_icon="🎯",
    layout="wide"
)

# 2. 샘플 데이터 생성
@st.cache_data
def load_data():
    data = {
        "Map": [
            "Ascent", "Ascent", "Ascent", "Ascent", "Ascent",
            "Bind", "Bind", "Bind", "Bind", "Bind",
            "Haven", "Haven", "Haven", "Haven", "Haven",
            "Lotus", "Lotus", "Lotus", "Lotus", "Lotus"
        ],
        "Agent": [
            "Sova", "Jett", "Kayo", "Omen", "Killjoy",
            "Raze", "Viper", "Brimstone", "Fade", "Skye",
            "Jett", "Sova", "Omen", "Killjoy", "Breach",
            "Raze", "Omen", "Killjoy", "Fade", "Viper"
        ],
        "Role": [
            "Initiator", "Duelist", "Initiator", "Controller", "Sentinel",
            "Duelist", "Controller", "Controller", "Initiator", "Initiator",
            "Duelist", "Initiator", "Controller", "Sentinel", "Initiator",
            "Duelist", "Controller", "Sentinel", "Initiator", "Controller"
        ],
        "PickRate": [
            88.5, 82.1, 64.3, 75.0, 71.2,
            85.4, 78.2, 60.1, 55.3, 52.0,
            80.0, 74.5, 68.2, 65.0, 50.1,
            82.0, 76.4, 70.1, 58.9, 54.2
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. 사이드바 - 메인 필터
st.sidebar.header("🔍 검색 및 필터")

all_maps = df["Map"].unique()
selected_map = st.sidebar.selectbox("맵을 선택하세요", all_maps)

all_roles = ["전체"] + list(df["Role"].unique())
selected_role = st.sidebar.selectbox("역할군 필터", all_roles)

# 데이터 필터링
filtered_df = df[df["Map"] == selected_map]
if selected_role != "전체":
    filtered_df = filtered_df[filtered_df["Role"] == selected_role]

filtered_df = filtered_df.sort_values(by="PickRate", ascending=False)

# 4. 메인 화면 구성
st.title("🎯 발로란트 맵별 인기 요원 Pick Rate")
st.markdown(f"**{selected_map}** 맵에서 주로 사용되는 요원 통계입니다.")

st.divider()

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(f"📊 {selected_map} 요원 픽률 차트")
    if not filtered_df.empty:
        # plotly 대신 Streamlit 자체 막대 차트(bar_chart) 사용
        chart_data = filtered_df.set_index("Agent")[["PickRate"]]
        st.bar_chart(chart_data)
    else:
        st.info("선택한 조건에 해당하는 요원이 없습니다.")

with col2:
    st.subheader("📋 상세 데이터")
    st.dataframe(
        filtered_df[["Agent", "Role", "PickRate"]].reset_index(drop=True),
        column_config={
            "Agent": "요원",
            "Role": "역할",
            "PickRate": st.column_config.NumberColumn("픽률 (%)", format="%.1f%%")
        },
        use_container_width=True
    )

# 5. 전체 맵 데이터 비교
st.divider()
st.subheader("🌐 전체 맵 최고 픽률 요원")

top_agent_per_map = df.loc[df.groupby("Map")["PickRate"].idxmax()]
st.table(top_agent_per_map[["Map", "Agent", "Role", "PickRate"]].reset_index(drop=True))
