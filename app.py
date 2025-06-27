import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="野球チーム成績アプリ", layout="wide")

# ログイン状態の保持
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ユーザー情報CSVの読み込み
def load_user_credentials():
    if os.path.exists("data/users.csv"):
        return pd.read_csv("data/users.csv")
    else:
        return pd.DataFrame(columns=["ユーザー名", "パスワード", "権限"])

users_df = load_user_credentials()

# ログイン画面
if not st.session_state.logged_in:
    st.title("🔐 ログイン画面")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        # 前後の空白を除去して比較
        users_df["ユーザー名"] = users_df["ユーザー名"].astype(str).str.strip()
        users_df["パスワード"] = users_df["パスワード"].astype(str).str.strip()
        username = username.strip()
        password = password.strip()
        user_row = users_df[(users_df["ユーザー名"] == username) & (users_df["パスワード"] == password)]
        if not user_row.empty:
            st.session_state.logged_in = True
            st.session_state.user_name = username
            st.session_state.role = user_row.iloc[0]["権限"]
            st.success(f"ようこそ、{username} さん！")
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています")

# ログイン後の画面
else:
    st.sidebar.title("メニュー")
    role = st.session_state.role
    user = st.session_state.user_name

    if role == "admin":
        menu = st.sidebar.radio("管理者メニュー", ["出欠確認", "ファイルのアップロード"])
        if menu == "出欠確認":
            st.title("📅 出欠確認（管理者）")
            st.write("※ 日程の出欠一覧や次回日程の作成")
            if os.path.exists("data/attendance.csv"):
                att_df = pd.read_csv("data/attendance.csv")
                st.dataframe(att_df)
            else:
                st.info("まだ出欠記録がありません")
        elif menu == "ファイルのアップロード":
            st.title("📤 成績ファイルアップロード")
            uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
            if uploaded_file:
                with open("data/成績表.xlsx", "wb") as f:
                    f.write(uploaded_file.read())
                st.success("ファイルを保存しました")

    elif role == "user":
        menu = st.sidebar.radio("ユーザーメニュー", ["出欠確認", "個人成績表", "TOP10"])

        if menu == "出欠確認":
            st.title("✅ 出欠確認（ユーザー）")
            today = datetime.date.today().isoformat()
            if st.button("出席する"):
                with open("data/attendance.csv", "a", encoding="utf-8-sig") as f:
                    f.write(f"{today},{user},出席\n")
                st.success("出席を記録しました")

        elif menu == "個人成績表":
            st.title("📊 個人成績表")
            if os.path.exists("data/成績表.xlsx"):
                df = pd.read_excel("data/成績表.xlsx")
                personal_df = df[df["名前"].replace(' ','') == user]
                st.dataframe(personal_df, use_container_width=True)
            else:
                st.warning("成績ファイルが見つかりません")

        elif menu == "TOP10":
            st.title("🏆 成績TOP10")
            if os.path.exists("data/成績表.xlsx"):
                df = pd.read_excel("data/成績表.xlsx")
                st.subheader("打率 TOP10")
                st.dataframe(df.sort_values(by="打率", ascending=False).head(10), use_container_width=True)
            else:
                st.warning("成績ファイルが見つかりません")

    # ログアウト
    if st.sidebar.button("ログアウト"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.role = None
        st.experimental_rerun()
