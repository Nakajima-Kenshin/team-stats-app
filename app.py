import streamlit as st
import pandas as pd

st.set_page_config(page_title="野球チーム成績アプリ", layout="centered")

# ボタンメニュー
st.title("📂 メニューを選択してください")
menu = st.radio(
    label="",
    options=[
        "🥇 ベスト10",
        "📊 成績",
        "📅 試合詳細",
        "📝 記録",
        "🏆 タイトル",
        "🎖️ 表彰",
        "🔐 管理者モード"
    ],
    horizontal=True
)

# データ読み込みの仮定
try:
    df = pd.read_excel("25-dasya.xlsx")
except:
    df = pd.DataFrame()

# 各メニューの表示処理
if menu == "🥇 ベスト10":
    st.title("🥇 ベスト10ランキング")
    if not df.empty:
        st.subheader("打率 TOP10")
        st.dataframe(df.sort_values(by="打率", ascending=False).head(10))

        st.subheader("打点 TOP10")
        st.dataframe(df.sort_values(by="打点", ascending=False).head(10))

        st.subheader("本塁打 TOP10")
        st.dataframe(df.sort_values(by="本塁打", ascending=False).head(10))
    else:
        st.warning("データが読み込まれていません")

elif menu == "📊 成績":
    st.title("📊 選手個人成績")
    st.dataframe(df)

elif menu == "📅 試合詳細":
    st.title("📅 試合別の成績")
    st.info("試合データがあれば詳細表示に対応します")

elif menu == "📝 記録":
    st.title("📝 チーム・個人記録")
    st.write("例：最多本塁打、連続打撃記録、最多第1打席好打率など")

elif menu == "🏆 タイトル":
    st.title("🏆 年間タイトル")
    st.write("例：首位打者、本塁率王、打点王など")

elif menu == "🎖️ 表彰":
    st.title("🎖️ 賞与者リスト")
    st.write("例：MVP、ベストナイン、労力賞など")

elif menu == "🔐 管理者モード":
    st.title("🔐 管理者モード")
    password = st.text_input("パスワードを入力", type="password")
    if password == "secret123":
        uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.success("ファイルを読み込みました")
    else:
        if password != "":
            st.error("パスワードが違います")
