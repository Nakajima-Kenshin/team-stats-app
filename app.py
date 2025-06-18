import streamlit as st
import pandas as pd

st.set_page_config(page_title="打者成績ビューア", layout="centered")
st.markdown("<h2 style='text-align: center;'>📱 2025年 打者成績ビューア</h2>", unsafe_allow_html=True)

# --- モード切替 ---
mode = st.radio("モードを選んでください", ["閲覧モード", "管理者モード 🔐"], horizontal=True)

# --- 管理者モード処理 ---
if mode == "管理者モード 🔐":
    password = st.text_input("パスワード", type="password")
    if password == "secret123":
        st.success("管理者モードでログイン成功！")
        uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("ファイルをアップロードしてください")
            st.stop()
    else:
        st.error("パスワードが間違っています")
        st.stop()
else:
    try:
        df = pd.read_excel("25-dasya.xlsx")
    except:
        st.error("既定ファイル '25-dasya.xlsx' が見つかりません。管理者モードでアップロードしてください。")
        st.stop()

# --- フィルターUI ---
st.subheader("🔍 選手成績を検索")

with st.expander("フィルター条件（タップして開く）"):
    filtered_df = df.copy()
    for col in df.columns:
        if df[col].dtype == 'object':
            keyword = st.text_input(f"{col} に含まれる文字列", key=col)
            if keyword:
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(keyword, case=False, na=False)]
        elif pd.api.types.is_numeric_dtype(df[col]):
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            selected = st.slider(f"{col} の範囲", min_val, max_val, (min_val, max_val), key=col)
            filtered_df = filtered_df[(df[col] >= selected[0]) & (df[col] <= selected[1])]

# --- 表の表示 ---
st.subheader(f"📊 フィルター結果（{len(filtered_df)} 件）")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# --- 打率ランキング（全体）---
if '打率' in df.columns:
    st.subheader("🏆 打率ランキング（全選手）")
    sorted_df = df.sort_values(by='打率', ascending=False)
    st.dataframe(sorted_df[['名前', '打率', '試合', '打席']], use_container_width=True, hide_index=True)

# --- 既定打席による打率ランキング（表のみ）---
st.subheader("✅ 既定打席以上の打率ランキング")

# 試合数と規定打席の計算（固定値 or 自動推定）
try:
    max_games = int(df["試合"].max())
except:
    max_games = 41  # 手動で設定

qualified_pa = round(max_games * 1.4, 1)
st.markdown(f"🔢 規定打席 = {max_games} 試合 × 1.4 = **{qualified_pa} 打席**")

qualified_df = df[df["打席"] >= qualified_pa]
qualified_df_sorted = qualified_df.sort_values(by='打率', ascending=False)

st.dataframe(qualified_df_sorted[['名前', '打率', '試合', '打席']], use_container_width=True, hide_index=True)
