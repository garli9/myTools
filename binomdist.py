import streamlit as st
from scipy.stats import binom

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
        format="%.3f"   # ← 表示桁数を固定
    )

cumulative = st.checkbox("累積確率（TRUE）", value=False)

# --- 計算 ---
if cumulative:
    prob = binom.cdf(x, n, p)
    st.success(f"✅ 累積確率 P(X ≤ {x}) = {prob:.6f}")
else:
    prob = binom.pmf(x, n, p)
    st.success(f"✅ 確率 P(X = {x}) = {prob:.6f}")