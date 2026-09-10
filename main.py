import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년 동안의 일별 박스오피스 데이터를 이용해 영화와 시간의 관계를 그래프로 살펴봅니다.")

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜(datetime) 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


try:
    df = load_data()

    st.success("영화 데이터를 불러왔습니다!")

    # ==================================================
    # 구역 1. 영화별 날짜에 따른 일관객 변화
    # ==================================================
    st.header("📈 1. 영화별 일관객 변화")

    st.write("영화를 선택하면 날짜에 따라 일관객 수가 어떻게 변했는지 확인할 수 있습니다.")

    # 영화 목록 만들기
    movie_list = sorted(df["영화명"].dropna().unique())

    # 드롭다운
    selected_movie = st.selectbox(
        "🎥 영화를 선택하세요",
        movie_list
    )

    # 선택한 영화 데이터
    movie_df = df[df["영화명"] == selected_movie].copy()

    # 날짜 순서대로 정렬
    movie_df = movie_df.sort_values("날짜")

    # Plotly 선 그래프
    fig = px.line(
        movie_df,
        x="날짜",
        y="일관객",
        markers=True,
        title=f"🎬 {selected_movie}의 날짜별 일관객 변화",
        labels={
            "날짜": "날짜",
            "일관객": "일관객 수"
        },
        hover_data={
            "날짜": "|%Y-%m-%d",
            "일관객": ":,"
        }
    )

    # 마우스를 올렸을 때 날짜와 관객 수가 보기 쉽게 표시되도록 설정
    fig.update_traces(
        hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br>"
                      "<b>일관객</b>: %{y:,}명"
                      "<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객 수(명)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 그래프 해석 문장 자리
    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다."
    )


    # ==================================================
    # 구역 2. 다음 그래프를 위한 공간
    # ==================================================
    st.divider()

    st.header("📊 2. 다음 그래프")

    st.write(
        "앞으로 시간과 관련된 새로운 영화 데이터 그래프를 이 구역에 추가할 수 있습니다."
    )

    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "여기에 두 번째 그래프를 보고 알 수 있는 내용을 작성합니다."
    )


    # ==================================================
    # 구역 3. 다음 그래프를 위한 공간
    # ==================================================
    st.divider()

    st.header("📉 3. 다음 그래프")

    st.write(
        "추가로 분석하고 싶은 영화 데이터 그래프를 이 구역에 넣을 수 있습니다."
    )

    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "여기에 세 번째 그래프를 보고 알 수 있는 내용을 작성합니다."
    )


    # ==================================================
    # 데이터 미리보기
    # ==================================================
    st.divider()

    with st.expander("📋 데이터 미리보기"):
        st.dataframe(df.head(20), use_container_width=True)

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
