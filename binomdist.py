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
    # 数値入力と分数入力の切り替えをわかりやすく
    st.write("成功確率 p の入力")
    p_text = st.text_input("小数または分数で入力（例：0.125 または 1/8）", value="0.100")

# --- p の解析 ---
try:
    if "/" in p_text:
        num, denom = p_text.split("/")
        p = float(num) / float(denom)
    else:
        p = float(p_text)
except Exception:
    st.error("⚠️ 有効な数値または分数を入力してください。")
    st.stop()

# --- バリデーション ---
if not (0.0 <= p <= 1.0):
    st.error("⚠️ 確率 p は 0〜1 の範囲で入力してください。")
    st.stop()

cumulative = st.checkbox("累積確率（TRUE）", value=False)

# --- 入力が変わるたびに自動で計算 ---
prob = binom.cdf(x, n, p) if cumulative else binom.pmf(x, n, p)

st.success(f"✅ 発生確率：P(X {'≤' if cumulative else '='} {x}) =  {prob:.8f}（p={p:.5f}）")

# --- 記録ボタン ---
if st.button("この結果を記録"):
    result = {
        "試行回数 n": n,
        "成功回数 x": x,
        "確率 p": round(p, 5),
        "結果": round(prob, 8)
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