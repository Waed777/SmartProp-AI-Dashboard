import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
st.sidebar.header("📁 Upload Your Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


st.set_page_config(
    page_title="SmartProp AI | Sample Insights",
    layout="wide"
)

st.title("📊 SmartProp AI – Real Estate AI Predictions")
st.subheader("Riyadh | AI-powered decision intelligence")

# -------------------------
# Sample Dataset
# -------------------------
np.random.seed(42)

data = pd.DataFrame({
    "Area": ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"],
    "Demand_Index": [90, 75, 65, 70],
    "Risk_Score": [35, 45, 60, 55],
    "Avg_Price": [8500, 7200, 6100, 6500]
})

# -------------------------
# Sidebar - User Input
# -------------------------
st.sidebar.header("📍 Select Area")
selected_area = st.sidebar.selectbox("Area", data["Area"])

area_data = data[data["Area"] == selected_area]

# -------------------------
# ML Model
# -------------------------
X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

model = LinearRegression()
model.fit(X, y)

predicted_price = model.predict(
    area_data[["Demand_Index", "Risk_Score"]]
)[0]

# -------------------------
# Decision Logic
# -------------------------
if area_data["Demand_Index"].values[0] > 80 and area_data["Risk_Score"].values[0] < 50:
    recommendation = "Strong Buy / Invest"
elif area_data["Risk_Score"].values[0] > 55:
    recommendation = "High Risk – Caution"
else:
    recommendation = "Hold / Monitor"

# -------------------------
# Display Metrics
# -------------------------
st.markdown("### 📌 Market Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Current Avg Price (SAR/m²)", int(area_data["Avg_Price"]))
col2.metric("AI Predicted Price (SAR/m²)", int(predicted_price))
col3.metric("AI Recommendation", recommendation)

# -------------------------
# Visualization
# -------------------------
st.markdown("### 📈 Price Comparison")

chart_data = pd.DataFrame({
    "Type": ["Current Price", "AI Predicted Price"],
    "Price": [area_data["Avg_Price"].values[0], predicted_price]
})

fig = px.bar(
    chart_data,
    x="Type",
    y="Price",
    title=f"Price Outlook – {selected_area}"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Insight
# -------------------------
st.markdown("### 🧠 AI Insight")
st.info(
    f"The AI model predicts a future average price of approximately "
    f"{int(predicted_price)} SAR/m² in {selected_area}. "
    f"Recommendation: {recommendation}."
)

# -------------------------
# CTA
# -------------------------
st.markdown("---")
st.markdown("### 🚀 Want full market access & real-time predictions?")
st.button("Book a Free Demo")


