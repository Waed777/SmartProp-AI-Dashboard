import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="SmartProp AI | Real Estate Intelligence",
    layout="wide"
)

# -------------------------------------------------
# Sidebar – Data Upload
# -------------------------------------------------
st.sidebar.header("📁 Upload Your Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

st.sidebar.markdown("""
**Required CSV Columns:**
- Area  
- Demand_Index  
- Risk_Score  
- Avg_Price  
""")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Data uploaded successfully")
else:
    data = pd.DataFrame({
        "Area": ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"],
        "Demand_Index": [90, 75, 65, 70],
        "Risk_Score": [35, 45, 60, 55],
        "Avg_Price": [8500, 7200, 6100, 6500]
    })

required_columns = {"Area", "Demand_Index", "Risk_Score", "Avg_Price"}
if not required_columns.issubset(data.columns):
    st.error("CSV must contain: Area, Demand_Index, Risk_Score, Avg_Price")
    st.stop()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📊 SmartProp AI – Real Estate Decision Intelligence")
st.subheader("Saudi Arabia | AI-powered market predictions")

# -------------------------------------------------
# Area Selection
# -------------------------------------------------
st.sidebar.header("📍 Select Area")
selected_area = st.sidebar.selectbox("Area", data["Area"].unique())
area_data = data[data["Area"] == selected_area]

# -------------------------------------------------
# ML Model
# -------------------------------------------------
X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

model = LinearRegression()
model.fit(X, y)

predicted_price = model.predict(
    area_data[["Demand_Index", "Risk_Score"]]
)[0]

# -------------------------------------------------
# Confidence Score
# -------------------------------------------------
confidence_score = max(
    70,
    100 - abs(predicted_price - area_data["Avg_Price"].values[0]) / 100
)

# -------------------------------------------------
# Investment Score & Decision Logic
# -------------------------------------------------
investment_score = (
    area_data["Demand_Index"].values[0] * 0.6
    - area_data["Risk_Score"].values[0] * 0.4
)

if investment_score > 40:
    recommendation = "🔥 Strong Investment Opportunity"
elif investment_score > 20:
    recommendation = "⚠️ Moderate – Monitor Closely"
else:
    recommendation = "❌ High Risk – Avoid"

# -------------------------------------------------
# Market Summary
# -------------------------------------------------
st.markdown("## 📌 Market Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Avg Price (SAR/m²)",
    int(area_data["Avg_Price"].values[0])
)

col2.metric(
    "AI Predicted Price (SAR/m²)",
    int(predicted_price)
)

col3.metric(
    "Prediction Confidence",
    f"{int(confidence_score)}%"
)

col4.metric(
    "Investment Score",
    int(investment_score)
)

# -------------------------------------------------
# Visualization
# -------------------------------------------------
st.markdown("## 📈 Price Outlook")

chart_data = pd.DataFrame({
    "Type": ["Current Price", "AI Predicted Price"],
    "Price": [
        area_data["Avg_Price"].values[0],
        predicted_price
    ]
})

fig = px.bar(
    chart_data,
    x="Type",
    y="Price",
    title=f"Price Comparison – {selected_area}",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# AI Insight
# -------------------------------------------------
st.markdown("## 🧠 AI Insight")
st.info(
    f"SmartProp AI forecasts an average price of approximately "
    f"{int(predicted_price)} SAR/m² in {selected_area}. "
    f"The demand and risk profile results in a recommendation of: "
    f"{recommendation}."
)

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------
st.markdown("## 🧾 Executive Summary")
st.success(
    f"In {selected_area}, SmartProp AI identifies a strong relationship "
    f"between demand intensity and pricing trends. With a prediction "
    f"confidence of {int(confidence_score)}%, the model suggests that "
    f"current market conditions represent: {recommendation}. "
    f"This insight is designed to support executive-level investment decisions."
)

# -------------------------------------------------
# CTA
# -------------------------------------------------
st.markdown("---")
st.markdown("## 🚀 Want full access to real-time AI insights?")
st.button("Book a Free Demo")


