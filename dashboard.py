import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(
    page_title="SmartProp AI | Sample Insights",
    layout="wide"
)

# Title
st.title("📊 SmartProp AI – Real Estate Market Insights (Sample)")
st.subheader("Riyadh | AI-powered sample analysis")

# Create sample data
np.random.seed(42)
areas = ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"]

data = pd.DataFrame({
    "Area": areas,
    "Average Price (SAR/m²)": np.random.randint(4000, 9000, size=4),
    "Demand Index": np.random.randint(60, 95, size=4),
    "Risk Score": np.random.randint(20, 70, size=4)
})

# Show table
st.markdown("### 📍 Market Overview")
st.dataframe(data, use_container_width=True)

# Charts
col1, col2 = st.columns(2)

with col1:
    fig_price = px.bar(
        data,
        x="Area",
        y="Average Price (SAR/m²)",
        title="Average Property Price by Area"
    )
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    fig_demand = px.line(
        data,
        x="Area",
        y="Demand Index",
        markers=True,
        title="Demand Forecast Index"
    )
    st.plotly_chart(fig_demand, use_container_width=True)

# Insight box
st.markdown("### 🧠 AI Insight")
st.info(
    "North Riyadh shows the strongest demand with moderate risk, "
    "making it a strong candidate for near-term residential investment."
)

# CTA
st.markdown("---")
st.markdown("### 🚀 Want full access to real-time insights?")
st.button("Book a Free Demo")

