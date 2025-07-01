import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ログイン", layout="centered")

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# ユーザー情報の読み込み
def load_users():
    if os.path.exists("data/users.csv"):
        df = pd.read_csv("data/users.csv")
        df["ユーザー名"] = df["ユーザー名"].astype(str).str.strip()
        df["パスワード"] = df["パスワード"].astype(str).str.strip()
        return df
    return pd.DataFrame(columns=["ユーザー名", "パスワード", "権限"])

st.title("🔐 ログイン")
username = st.text_input("ユーザー名")
password = st.text_input("パスワード", type="password")

users_df = load_users()

if st.button("ログイン"):
    username = username.strip()
    password = password.strip()
    user_row = users_df[(users_df["ユーザー名"] == username) & (users_df["パスワード"] == password)]
    if not user_row.empty:
        st.session_state.user_name = username
        st.session_state.role = user_row.iloc[0]["権限"]
        if st.session_state.role == "admin":
            st.switch_page("pages/admin_app.py")
        else:
            st.switch_page("pages/user_app.py")
    else:
        st.error("ユーザー名またはパスワードが間違っています")
