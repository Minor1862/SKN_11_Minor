import streamlit as st
import pandas as pd

# CSV 파일 불러오기
def load_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    return pd.concat(dataframes, ignore_index=True)

# 데이터 로드
file_paths = ["ev_or_faq_data.csv", "kia_faq_data.csv", "chevrolet_faq_data.csv"]  # CSV 파일 경로 리스트
try:
    df = load_data(file_paths)
    st.success("FAQ 데이터 업데이트 완료!")
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    df = None

if df is not None:
    # 카테고리 선택
    categories = df["category"].unique()
    selected_category = st.selectbox("카테고리를 선택하세요", categories)
    
    # 소분류 선택
    subcategories = df[df["category"] == selected_category]["question"].unique()
    selected_subcategory = st.selectbox("질문을을 선택하세요", subcategories)
    
    # 해당 소분류에 대한 값 표시
    values = df[(df["category"] == selected_category) & (df["question"] == selected_subcategory)]["answer"]
    st.write("### 답변 내용 : ")
    value_text = "\n".join(values.astype(str).to_list())
    st.text_area("answer", value_text, height=200)
