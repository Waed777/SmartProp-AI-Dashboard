import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="AI Smart | Real Estate AI Engine",
    layout="wide"
)

# =================================================
# TITLE
# =================================================
st.title("🧠 AI Smart – Real Estate Decision Engine")
st.caption("AI-powered investment intelligence | Vision 2030")

st.markdown("---")

# =================================================
# SAMPLE DATA (you can replace later)
# =================================================
data = pd.DataFrame({
    "Area": ["North Riyadh"] * 6,
    "Year": [2020, 2021, 2022, 2023, 2024, 2025],
    "Demand_Index": [60, 65, 70, 80, 85, 90],
    "Risk_Score": [55, 50, 48, 45, 40, 35],
    "Avg_Price": [6200, 6500, 6900, 7600, 8200, 8800]
})

# =================================================
# AI ENGINE (REAL BRAIN)
# =================================================
X = data[["Demand_Index", "Risk_Score", "Year"]]
y = data["Avg_Price"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression())
])

model.fit(X, y)

# =================================================
# SIDEBAR – SIMULATION CONTROLS
# =================================================
st.sidebar.header("🎛️ Simulation Controls")

year = st.sidebar.slider("Target Year", 2025, 2035, 2030)
demand = st.sidebar.slider("Demand Index", 50, 100, 90)
risk = st.sidebar.slider("Risk Score", 20, 80, 30)

# =================================================
# AI PREDICTION
# =================================================
input_df = pd.DataFrame([[demand, risk, year]], columns=X.columns)
predicted_price = model.predict(input_df)[0]

investment_score = round((0.7 * demand) - (0.4 * risk), 2)
confidence = max(70, 100 - abs(predicted_price - data["Avg_Price"].iloc[-1]) / 120)

# =================================================
# OUTPUT – INVESTOR VIEW
# =================================================
c1, c2, c3, c4 = st.columns(4)

c1.metric("AI Predicted Price (SAR/m²)", f"{int(predicted_price)}")
c2.metric("Investment Score", investment_score)
c3.metric("Prediction Confidence", f"{int(confidence)}%")
c4.metric(
    "Verdict",
    "STRONG BUY" if investment_score > 40 else "MONITOR"
)

st.markdown("---")

# =================================================
# EXPLAINABLE AI (STORYTELLING)
# =================================================
st.subheader("🧠 AI Decision Explanation")

if demand > 75:
    st.write("• High demand is a strong positive driver for price growth.")
else:
    st.write("• Moderate demand limits upside potential.")

if risk > 60:
    st.write("• Elevated risk is suppressing valuation.")
else:
    st.write("• Risk level is within acceptable investment range.")

st.write(
    f"• For year **{year}**, the AI estimates a fair value of "
    f"**{int(predicted_price)} SAR/m²** based on historical behavior."
)

# =================================================
# RISK SIMULATION (MONTE CARLO LIGHT)
# =================================================
st.markdown("---")
st.subheader("📉 Risk Simulation (Multiple Futures)")

simulated_prices = []

for _ in range(500):
    d = np.random.normal(demand, 5)
    r = np.random.normal(risk, 5)
    simulated_prices.append(
        model.predict([[d, r, year]])[0]
    )

st.write({
    "Min": int(np.min(simulated_prices)),
    "Expected": int(np.mean(simulated_prices)),
    "Max": int(np.max(simulated_prices))
})

# =================================================
# EXECUTIVE SUMMARY
# =================================================
st.markdown("---")
st.subheader("🧾 Executive Summary")

st.success(
    f"""
    AI Smart analysis indicates that **North Riyadh** in **{year}**
    represents a **{'high-potential investment' if investment_score > 40 else 'moderate-risk scenario'}**.

    The projected value is **{int(predicted_price)} SAR/m²**
    with an AI confidence level of **{int(confidence)}%**.

    This engine is designed for strategic, long-term investment decisions
    aligned with Saudi Vision 2030.
    """
)
