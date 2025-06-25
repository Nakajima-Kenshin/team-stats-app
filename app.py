import streamlit as st
import pandas as pd

st.set_page_config(page_title="野球チーム成績アプリ", layout="centered")

# セッション状態でメニューを管理
if "menu" not in st.session_state:
    st.session_state.menu = "ホーム"

st.title("📂 メニューを選択してください")

# ボタンメニュー（画面上）
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🥇 ベスト10"):
        st.session_state.menu = "🥇 ベスト10"
    if st.button("📅 試合詳細"):
        st.session_state.menu = "📅 試合詳細"
with col2:
    if st.button("📊 成績"):
        st.session_state.menu = "📊 成績"
    if st.button("📝 記録"):
        st.session_state.menu = "📝 記録"
with col3:
    if st.button("🏆 タイトル"):
        st.session_state.menu = "🏆 タイトル"
    if st.button("🎖️ 表彰"):
        st.session_state.menu = "🎖️ 表彰"

# 管理者モード（独立配置）
if st.button("🔐 管理者モード"):
    st.session_state.menu = "🔐 管理者モード"

# データ読み込みの仮定
try:
    df = pd.read_excel("25-dasya.xlsx")
except:
    df = pd.DataFrame()

# 各メニューの表示処理
menu = st.session_state.menu

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
    if "df" in st.session_state:
    	st.dataframe(st.session_state.df)

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
    if password == "Squalls":
    	st.success("管理者としてログインしました")
        uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success("ファイルを読み込みました")
        else:
        	st.stop()
    else:
        if password != "":
            st.error("パスワードが違います")