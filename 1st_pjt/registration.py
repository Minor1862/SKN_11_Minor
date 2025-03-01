import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
# import plotly.express as px


font_path = 'C:/Windows/Fonts/NanumGothic.ttf'  # 폰트 파일 경로
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

def run():
    st.title("📊 등록 현황")

    # Markdown 문법으로 제목 및 서브 제목 꾸미기
    st.markdown("""
    <h3 style='color: #FF6347;'>지역별 및 연료별 등록 현황</h3>
    친환경 자동차의 최신 현황 데이터를 이용해 트렌드를 분석합니다.
    """, unsafe_allow_html=True)
    st.markdown("<h5 style='font-size: 16px;'>국내 지역별 / 연료별 자동차의 등록 결과를 확인할 수 있습니다.</h5>", unsafe_allow_html=True)
    # 텍스트 강조 및 정보 표시
    st.info("💡 **이 분석은 2024년 기준으로 지역별, 등록 현황을 시각화한 것입니다.**")



    # 데이터 확인
    st.write("📋 데이터 미리보기", df.head())

    # 필터 선택
    st.sidebar.header("필터 선택")
    selected_years = st.sidebar.multiselect("연도 선택", df["연도"].unique(), default=df["연도"].unique())
    selected_regions = st.sidebar.multiselect("지역 선택", df["지역"].unique(), default=df["지역"].unique())

    # 필터링
    filtered_df = df[(df["연도"].isin(selected_years)) & (df["지역"].isin(selected_regions))]

    # 합계 연도별 판매량 비교
    yearly_sales = filtered_df.groupby("연도")["등록대수"].sum().reset_index()

    # 2024년의 지역별 판매량 비교
    sales_2024 = filtered_df[filtered_df["연도"] == "2024"].groupby("지역")["등록대수"].sum().reset_index()

    # 시각화
    #st.title("📊 연도별 & 지역별 자동차 등록 현황")

    # 📈 연도별 판매량 비교 차트
    st.subheader("📅 연도별 판매량 비교")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=yearly_sales, x="연도", y="등록대수", palette="coolwarm", ax=ax1)
    ax1.set_xlabel("연도")
    ax1.set_ylabel("등록대수")
    ax1.set_title("연도별 자동차 등록 현황")
    st.pyplot(fig1)

    # 📈 2024년 지역별 판매량 비교 차트
    if not sales_2024.empty:
        st.subheader("📍 2024년 지역별 판매량 비교")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.barplot(data=sales_2024, x="지역", y="등록대수", palette="viridis", ax=ax2)
        ax2.set_xlabel("지역")
        ax2.set_ylabel("등록대수")
        ax2.set_title("2024년 지역별 자동차 등록 현황")
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)  # 지역명이 길 경우 가독성 향상
        st.pyplot(fig2)

    # st.subheader("📊 연도별 & 지역별 자동차 등록 현황")
    # fig3, ax3 = plt.subplots(figsize=(12, 6))
    # sns.barplot(data=filtered_df, x="연도", y="등록대수", hue="지역", palette="magma", ax=ax3)
    # ax3.set_xlabel("연도")
    # ax3.set_ylabel("등록대수")
    # ax3.set_title("연도별 & 지역별 자동차 등록 현황")
    # ax3.legend(title="지역")
    # st.pyplot(fig3)


st.cache_data
def load_data():
    df = pd.read_csv("125704.csv", encoding='euc-kr', header=None)  # 적절한 인코딩으로 수정
    df.columns = ["지역"] + df.iloc[2, 1:].tolist()  # 3번째 행(인덱스 2)을 연도로 설정
    df = df.iloc[3:].reset_index(drop=True)  # 실제 데이터는 4번째 행부터 시작
    df = df.melt(id_vars=["지역"], var_name="연도", value_name="등록대수")  # 연도별 데이터 변환
    df["등록대수"] = pd.to_numeric(df["등록대수"], errors="coerce")  # 숫자 변환
    return df

df = load_data()