import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(page_title="管理者メニュー", layout="wide")

st.title("🛠 管理者メニュー")

if "user_name" not in st.session_state or st.session_state.role != "admin":
    st.warning("ログインしてください")
    st.stop()

menu = st.selectbox("メニュー選択", ["出欠確認", "成績ファイルのアップロード"])

if menu == "出欠確認":
    if os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")
        st.dataframe(df)
    else:
        st.info("出欠記録がありません")

elif menu == "成績ファイルのアップロード":
    uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
    if uploaded_file:
        with open("records.xlsx", "wb") as f:
            f.write(uploaded_file.read())
        st.success("ファイルを保存しました")

if st.button("ログアウト"):
    st.session_state.user_name = ""
    st.session_state.role = ""
    st.switch_page("login_app")
