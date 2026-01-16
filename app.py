import streamlit as st
import pandas as pd
from datetime import datetime

# ページの設定
st.set_page_config(page_title="警備応援マッチング", layout="centered")

# --- データ管理（アプリが起動している間保持されます） ---
if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame([
        {"会社名": "警備A社", "空き人数": 5, "更新時間": "2026-01-16 10:00"},
        {"会社名": "警備B社", "空き人数": 0, "更新時間": "2026-01-16 11:30"},
    ])

st.title("🛡️ 警備隊員・共同応援マッチング")
st.info("提携業者間で「人手が余っている会社」と「足りない会社」を可視化します。")

# --- 1. 自社の状況を更新する（供給側） ---
with st.expander("➕ 自社の空き状況を登録・更新する", expanded=True):
    with st.form("update_form"):
        company_name = st.selectbox("自社名を選択", ["警備A社", "警備B社", "警備C社", "警備D社", "警備E社"])
        available_count = st.number_input("応援に出せる人数（現在空いている人数）", min_value=0, step=1)
        submit_btn = st.form_submit_button("情報を更新する")
        
        if submit_btn:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            if company_name in st.session_state.fleet_data["会社名"].values:
                st.session_state.fleet_data.loc[st.session_state.fleet_data["会社名"] == company_name, ["空き人数", "更新時間"]] = [available_count, now]
            else:
                new_data = {"会社名": company_name, "空き人数": available_count, "更新時間": now}
                st.session_state.fleet_data = pd.concat([st.session_state.fleet_data, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"{company_name}の情報を更新しました！")

st.divider() # プログラム用の正しい区切り線

# --- 2. 空き状況一覧（需要側） ---
st.subheader("🌐 現在の応援可能リスト")

# 人数が1人以上の会社のみ表示
df = st.session_state.fleet_data
available_list = df[df["空き人数"] > 0]

if not available_list.empty:
    # テーブル表示
    st.dataframe(available_list, use_container_width=True)
    
    # 簡易予約フォーム
    st.write("---")
    st.write("### 🤝 応援を依頼する")
    target_company = st.selectbox("依頼先の会社を選択", available_list["会社名"])
    request_num = st.number_input("依頼したい人数", min_value=1, step=1)
    
    if st.button("仮予約を送る"):
        st.balloons()
        st.warning(f"【送信完了】{target_company} へ {request_num} 名の仮予約依頼を通知しました。（※デモ用メッセージ）")
else:
    st.write("現在、応援可能な会社（空き隊員）はありません。")
