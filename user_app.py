import streamlit as st
import pandas as pd
import os
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="ユーザーメニュー", layout="wide")

st.title("📱 ユーザーメニュー")

if "user_name" not in st.session_state or st.session_state.role != "user":
    st.warning("ログインしてください")
    st.stop()

user = st.session_state.user_name
menu = st.selectbox("メニュー選択", ["出欠登録", "個人成績", "TOP10"])

if menu == "出欠登録":
    today = datetime.date.today().isoformat()
    if st.button("✅ 出席する"):
        with open("attendance.csv", "a", encoding="utf-8-sig") as f:
            f.write(f"{today},{user},出席\n")
        st.success("出席を記録しました")

elif menu == "個人成績":
    if os.path.exists("data/成績表.xlsx"):
        df = pd.read_excel("data/成績表.xlsx")
        df["名前"] = df["名前"].astype(str).str.replace(r"[ 　]", "", regex=True)
        user_name_cleaned = user.replace(" ", "").replace("　", "")
        st.subheader("📋 個人成績（名前列固定）")
        filtered_df = df[df["名前"] == user_name_cleaned]
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_column("名前", pinned="left")
        gb.configure_default_column(resizable=True)
        grid_options = gb.build()
        AgGrid(filtered_df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)
    else:
        st.warning("成績ファイルが見つかりません")

elif menu == "TOP10":
    if os.path.exists("data/成績表.xlsx"):
        df = pd.read_excel("data/成績表.xlsx")
        st.subheader("打率 TOP10（名前列固定）")
        top10_df = df.sort_values(by="打率", ascending=False).head(10)
        gb = GridOptionsBuilder.from_dataframe(top10_df)
        gb.configure_column("名前", pinned="left")
        gb.configure_default_column(resizable=True)
        grid_options = gb.build()
        AgGrid(top10_df, gridOptions=grid_options, height=300, fit_columns_on_grid_load=True)
    else:
        st.warning("成績ファイルが見つかりません")

if st.button("ログアウト"):
    st.session_state.user_name = ""
    st.session_state.role = ""
    st.switch_page("login_app")
