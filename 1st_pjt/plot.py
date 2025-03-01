import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 로드 및 전처리
@st.cache_data
def load_data():
    df = pd.read_csv("125704.csv", encoding='euc-kr', header=None)  # 적절한 인코딩으로 수정
    df.columns = ["지역"] + df.iloc[2, 1:].tolist()  # 3번째 행(인덱스 2)을 연도로 설정
    df = df.iloc[3:].reset_index(drop=True)  # 실제 데이터는 4번째 행부터 시작
    df = df.melt(id_vars=["지역"], var_name="연도", value_name="등록대수")  # 연도별 데이터 변환
    df["등록대수"] = pd.to_numeric(df["등록대수"], errors="coerce")  # 숫자 변환
    return df

df = load_data()

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
st.title("📊 연도별 & 지역별 자동차 등록 현황")

# 합계 연도별 판매량 비교 데이터
st.write("📅 **연도별 판매량 합계**", yearly_sales)

# 2024년의 지역별 판매량 비교 데이터
st.write("📅 **2024년 지역별 판매량**", sales_2024)

# 바 차트 시각화 (연도별 & 지역별)
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_df, x="연도", y="등록대수", hue="지역", palette="viridis")
plt.xlabel("연도")
plt.ylabel("등록대수")
plt.title("연도별 & 지역별 자동차 등록 현황")
plt.legend(title="지역")

# 시각화 결과 출력
st.pyplot(plt)
