import streamlit as st
import pandas as pd

st.title("2025年 野球チーム 個人成績ビューア")

uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("成績表")
    st.dataframe(df)

    if '打率' in df.columns:
        st.subheader("打率ランキング")
        df_sorted = df.sort_values(by='打率', ascending=False)
        st.dataframe(df_sorted)