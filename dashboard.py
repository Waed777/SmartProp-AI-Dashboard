import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
import time

# =================================================
# Page Config
# =================================================
st.set_page_config(
    page_title="AI Smart | Vision 2030 Real Estate",
    layout="wide"
)

# =================================================
# CSS - Neon Glow & Particles Background
# =================================================
st.markdown("""
<style>
@keyframes glow {
  0% { text-shadow: 0 0 5px #fff, 0 0 10px #ff00de, 0 0 20px #ff00de, 0 0 30px #ff00de;}
  50% { text-shadow: 0 0 10px #fff, 0 0 20px #ff00de, 0 0 30px #ff00de, 0 0 40px #ff00de;}
  100% { text-shadow: 0 0 5px #fff, 0 0 10px #ff00de, 0 0 20px #ff00de, 0 0 30px #ff00de;}
}
.glow {
  font-size: 60px;
  font-weight: bold;
  color: #fff;
  animation: glow 1.5s infinite;
  text-align: center;
}
body {
  background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
  color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="glow">AI Smart - Vision 2030</div>', unsafe_allow_html=True)

# =================================================
# Sidebar - Language + Upload
# =================================================
language = st.sidebar.selectbox("🌐 Language | اللغة", ["English", "العربية"])

def t(en, ar):
    return en if language == "English" else ar

st.sidebar.header(t("📁 Upload Your Data", "📁 رفع البيانات"))
uploaded_file = st.sidebar.file_uploader(t("Upload CSV file", "ارفع ملف CSV"), type=["csv"])

# =================================================
# Load Data
# =================================================
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.DataFrame({
        "Area": ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"],
        "Demand_Index": [90, 75, 65, 70],
        "Risk_Score": [35, 45, 60, 55],
        "Avg_Price": [8500, 7200, 6100, 6500]
    })

# =================================================
# Area Selection
# =================================================
st.sidebar.header(t("📍 Select Area", "📍 اختر المنطقة"))
selected_area = st.sidebar.selectbox(t("Area", "المنطقة"), data["Area"].unique())
area_data = data[data["Area"] == selected_area]

# =================================================
# ML Prediction
# =================================================
X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

pipeline = Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])
pipeline.fit(X, y)
predicted_price = pipeline.predict(area_data[["Demand_Index", "Risk_Score"]])[0]

# =================================================
# Investment Score + Confidence
# =================================================
investment_score = area_data['Demand_Index'].values[0]*0.65 - area_data['Risk_Score'].values[0]*0.35
confidence_score = max(75, 100 - abs(predicted_price - area_data['Avg_Price'].values[0])/120)

# =================================================
# Animated KPI Cards
# =================================================
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("Current Price", "السعر الحالي"), f"{int(area_data['Avg_Price'])} SAR")
c2.metric(t("AI Predicted Price", "السعر المتوقع"), f"{int(predicted_price)} SAR")
c3.metric(t("Investment Score", "درجة الاستثمار"), int(investment_score))
c4.metric(t("Prediction Confidence", "دقة التنبؤ"), f"{int(confidence_score)}%")

# =================================================
# Scenario Simulation Slider
# =================================================
demand_slider = st.slider(t("Simulate Demand", "تجربة الطلب"), 50, 120, int(area_data['Demand_Index']))
risk_slider = st.slider(t("Simulate Risk", "تجربة المخاطرة"), 20, 80, int(area_data['Risk_Score']))
simulated_price = pipeline.predict([[demand_slider, risk_slider]])[0]
st.info(t(f"Simulated price: {int(simulated_price)} SAR/m²", f"السعر التجريبي: {int(simulated_price)} ريال/م²"))

# =================================================
# Animated Bar Chart with Trend
# =================================================
st.markdown(t("## 📊 Price & Investment Projection", "## 📊 توقعات السعر والاستثمار"))
chart_data = pd.DataFrame({
    t("Type", "النوع"): [t("Current", "الحالي"), t("AI Prediction", "توقع الذكاء الاصطناعي"), t("Simulated", "تجريبي")],
    t("Price", "السعر"): [area_data['Avg_Price'].values[0], predicted_price, simulated_price]
})
fig = px.bar(chart_data, x=chart_data.columns[0], y=chart_data.columns[1], text_auto=True, color=chart_data.columns[0], color_discrete_map={t("Current", "الحالي"):'blue', t("AI Prediction", "توقع الذكاء الاصطناعي"):'orange', t("Simulated", "تجريبي"):'green'})
fig.update_traces(marker_line_width=3, opacity=0.8)
st.plotly_chart(fig, use_container_width=True)

# =================================================
# AI Chat Assistant with Investment Storytelling
# =================================================
st.markdown(t("## 💬 AI Investment Assistant", "## 💬 مساعد استثماري ذكي"))
user_question = st.text_input(t("Ask a question...", "اكتب سؤالك هنا..."))

def ai_chat_response(question, area_data, predicted_price):
    if not question:
        return ""
    if 'why' in question.lower() or 'ليش' in question:
        return t(f"The recommendation is based on demand ({area_data['Demand_Index'].values[0]}) and risk ({area_data['Risk_Score'].values[0]}).", f"التوصية مبنية على مستوى الطلب ({area_data['Demand_Index'].values[0]}) والمخاطرة ({area_data['Risk_Score'].values[0]}).")
    if 'good' in question.lower() or 'استثمار' in question:
        return t(f"Predicted price: {int(predicted_price)} SAR/m², high potential ROI.", f"السعر المتوقع: {int(predicted_price)} ريال/م²، عائد محتمل مرتفع.")
    if 'simulate' in question.lower() or 'تجربة' in question:
        simulated_price = predicted_price * 1.05
        return t(f"Simulated price with increased demand: {int(simulated_price)} SAR/m²", f"السعر التجريبي مع زيادة الطلب: {int(simulated_price)} ريال/م²")
    return t("AI insight based on demand, risk, and 2030 vision.", "تحليل الذكاء الاصطناعي بناءً على الطلب والمخاطرة ورؤية 2030.")

if user_question:
    with st.spinner(t("Thinking...", "يتم المعالجة...")):
        answer = ai_chat_response(user_question, area_data, predicted_price)
    st.success(answer)

# =================================================
# CTA Animated Button
# =================================================
st.markdown("---")
if st.button(t("🚀 Subscribe Now", "🚀 اشترك الآن")):
    st.balloons()
