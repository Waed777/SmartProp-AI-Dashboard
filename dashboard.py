import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

st.set_page_config(
    page_title="SmartProp AI | Real Estate Intelligence",
    layout="wide"
)

lang = st.sidebar.radio("🌍 Language / اللغة", ["English", "العربية"])

def t(en, ar):
    return en if lang == "English" else ar

st.sidebar.header(t("📁 Upload Your Data", "📁 رفع البيانات"))
uploaded_file = st.sidebar.file_uploader(
    t("Upload CSV file", "ارفع ملف CSV"),
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.DataFrame({
        "Area": ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"],
        "Demand_Index": [90, 75, 65, 70],
        "Risk_Score": [35, 45, 60, 55],
        "Avg_Price": [8500, 7200, 6100, 6500]
    })

required_columns = {"Area", "Demand_Index", "Risk_Score", "Avg_Price"}
if not required_columns.issubset(data.columns):
    st.error(t("CSV must contain Area, Demand_Index, Risk_Score, Avg_Price",
               "يجب أن يحتوي الملف على الأعمدة المطلوبة"))
    st.stop()

st.title("📊 SmartProp AI")
st.subheader(t("AI-powered Real Estate Intelligence Platform",
               "منصة ذكاء اصطناعي لتحليل الاستثمار العقاري"))

st.sidebar.header(t("📍 Select Area", "📍 اختر المنطقة"))
selected_area = st.sidebar.selectbox("Area", data["Area"].unique())
area_data = data[data["Area"] == selected_area]

X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

model = LinearRegression()
model.fit(X, y)
predicted_price = model.predict(area_data[["Demand_Index", "Risk_Score"]])[0]

investment_score = area_data["Demand_Index"].values[0]*0.6 - area_data["Risk_Score"].values[0]*0.4

if investment_score > 40:
    recommendation = t("🔥 Strong Investment", "🔥 استثمار قوي")
elif investment_score > 20:
    recommendation = t("⚠️ Moderate Risk", "⚠️ مخاطرة متوسطة")
else:
    recommendation = t("❌ High Risk", "❌ مخاطرة عالية")

st.markdown("## 📌 " + t("Market Summary", "ملخص السوق"))
c1, c2, c3 = st.columns(3)
c1.metric(t("Current Price (SAR/m²)", "السعر الحالي"), int(area_data["Avg_Price"].values[0]))
c2.metric(t("AI Predicted Price", "السعر المتوقع"), int(predicted_price))
c3.metric(t("Recommendation", "التوصية"), recommendation)

chart_data = pd.DataFrame({
    t("Type", "النوع"): [t("Current", "حالي"), t("Predicted", "متوقع")],
    t("Price", "السعر"): [area_data["Avg_Price"].values[0], predicted_price]
})

fig = px.bar(chart_data, x=chart_data.columns[0], y=chart_data.columns[1], text_auto=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("## 💬 " + t("AI Assistant", "مساعد ذكي"))
question = st.text_input(t("Ask about investment decision...", "اسألي عن قرار الاستثمار..."))
if question:
    st.success(t(f"Based on demand and risk, recommendation is: {recommendation}",
                 f"بناءً على الطلب والمخاطرة، التوصية هي: {recommendation}"))

st.markdown("---")
st.button(t("Book Free Demo", "احجزي عرض تجريبي"))
