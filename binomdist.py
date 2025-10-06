import streamlit as st
from scipy.stats import binom
import pandas as pd

st.set_page_config(page_title="二項分布計算ツール", page_icon="🎲")

st.title("🎲 二項分布計算ツール")

# --- 入力欄 ---
col1, col2, col3 = st.columns(3)
with col1:
    n = st.number_input("試行回数 n", min_value=1, value=10, step=1)
with col2:
    x = st.number_input("成功回数 x", min_value=0, value=0, step=1)
with col3:
    p = st.number_input(
        "成功確率 p",
        min_value=0.000,
        max_value=1.000,
        value=0.100,
        step=0.001,
        format="%.3f"
    )

cumulative = st.checkbox("累積確率（TRUE）", value=False)

# --- 入力が変わるたびに自動で計算 ---
prob = binom.cdf(x, n, p) if cumulative else binom.pmf(x, n, p)
mode = "累積" if cumulative else "単発"

st.success(f"✅ {mode}確率：P(X {'≤' if cumulative else '='} {x}) = {prob:.6f}")

# --- 記録ボタン ---
if st.button("この結果を記録"):
    result = {
        "試行回数 n": n,
        "成功回数 x": x,
        "確率 p": round(p, 3),
        "結果": round(prob, 6)
    }

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.insert(0, result)
    st.session_state.history = st.session_state.history[:5]  # 最新5件に制限

# --- 履歴テーブル ---
if "history" in st.session_state and len(st.session_state.history) > 0:
    st.subheader("📋 記録された結果（最大5件）")
    df = pd.DataFrame(st.session_state.history)
    st.table(df)

st.write("---")
st.caption("Powered by Streamlit + SciPy ｜ 結果は自動計算され、ボタンで履歴に記録されます。")