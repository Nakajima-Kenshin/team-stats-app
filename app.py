import streamlit as st
import pandas as pd

st.title("2025年 野球チーム 成績ビューア")

# --- モード切替（パスワードベース） ---
mode = st.radio("モードを選択してください", ["閲覧モード", "管理者モード 🔐"])

if mode == "管理者モード 🔐":
    password = st.text_input("管理者パスワードを入力", type="password")
    if password == "squalls_owner":  # 🔐 パスワードを自由に設定
        st.success("管理者モードでログインしました")

        # 管理者だけがExcelをアップロードできる
        uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.success("ファイルを読み込みました")
        else:
            st.stop()
    else:
        st.error("パスワードが違います")
        st.stop()
else:
    # 閲覧モードでは既存のファイルを読み込む
    df = pd.read_excel("25-dasya.xlsx")

# --- 表の表示 ---
st.subheader("個人成績")
st.dataframe(df)

# --- 打率順ソート ---
if '打率' in df.columns:
    st.subheader("打率ランキング")
    df_sorted = df.sort_values(by='打率', ascending=False)
    st.dataframe(df_sorted)
