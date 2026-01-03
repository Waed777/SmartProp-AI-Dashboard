import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px


st.set_page_config(
    page_title="SmartProp AI | Real Estate Intelligence",
    layout="wide"
)

# =================================================
# Language Toggle
# =================================================
lang = st.sidebar.radio("🌍 Language / اللغة", ["English", "العربية"])

def t(en, ar):
    return en if lang == "English" else ar

# =================================================
# Sidebar – Data Upload
# =================================================
st.sidebar.header(t("📁 Upload Your Data", "📁 رفع البيانات"))
uploaded_file = st.sidebar.file_uploader(
    t("Upload CSV file", "ارفع ملف CSV"),
    type=["csv"]
)

st.sidebar.markdown(t(
    """
    **Required CSV Columns:**
    - Area
    - Demand_Index
    - Risk_Score
    - Avg_Price
    """,
    """
    **الأعمدة المطلوبة:**
    - Area
    - Demand_Index
    - Risk_Score
    - Avg_Price
    """
))

# =================================================
# Load Data
# =================================================
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success(t("✅ Data uploaded successfully", "✅ تم رفع البيانات بنجاح"))
else:
    data = pd.DataFrame({
        "Area": ["North Riyadh", "East Riyadh", "West Riyadh", "South Riyadh"],
        "Demand_Index": [90, 75, 65, 70],
        "Risk_Score": [35, 45, 60, 55],
        "Avg_Price": [8500, 7200, 6100, 6500]
    })

required_columns = {"Area", "Demand_Index", "Risk_Score", "Avg_Price"}
if not required_columns.issubset(data.columns):
    st.error(t(
        "CSV must contain: Area, Demand_Index, Risk_Score, Avg_Price",
        "يجب أن يحتوي الملف على الأعمدة المطلوبة"
    ))
    st.stop()

# =================================================
# Header
# =================================================
st.title("📊 SmartProp AI")
st.subheader(t(
    "AI-powered Real Estate Decision Intelligence",
    "ذكاء اصطناعي لدعم قرارات الاستثمار العقاري"
))

# =================================================
# Area Selection
# =================================================
st.sidebar.header(t("📍 Select Area", "📍 اختر المنطقة"))
selected_area = st.sidebar.selectbox("Area", data["Area"].unique())
area_data = data[data["Area"] == selected_area]

# =================================================
# ML Model
# =================================================
X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

model = LinearRegression()
model.fit(X, y)

predicted_price = model.predict(
    area_data[["Demand_Index", "Risk_Score"]]
)[0]

# =================================================
# Confidence Score
# =================================================
confidence_score = max(
    70,
    100 - abs(predicted_price - area_data["Avg_Price"].values[0]) / 100
)

# =================================================
# Investment Score & Decision Logic
# =================================================
investment_score = (
    area_data["Demand_Index"].values[0] * 0.6
    - area_data["Risk_Score"].values[0] * 0.4
)

if investment_score > 40:
    recommendation = t("🔥 Strong Investment Opportunity", "🔥 فرصة استثمار قوية")
elif investment_score > 20:
    recommendation = t("⚠️ Moderate – Monitor Closely", "⚠️ متوسطة – تحتاج متابعة")
else:
    recommendation = t("❌ High Risk – Avoid", "❌ مخاطرة عالية – يفضل تجنبها")

# =================================================
# Market Summary
# =================================================
st.markdown("## 📌 " + t("Market Summary", "ملخص السوق"))

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    t("Current Avg Price (SAR/m²)", "السعر الحالي (ريال/م²)"),
    int(area_data["Avg_Price"].values[0])
)

col2.metric(
    t("AI Predicted Price (SAR/m²)", "السعر المتوقع بالذكاء الاصطناعي"),
    int(predicted_price)
)

col3.metric(
    t("Prediction Confidence", "دقة التنبؤ"),
    f"{int(confidence_score)}%"
)

col4.metric(
    t("Investment Score", "مؤشر الاستثمار"),
    int(investment_score)
)

# =================================================
# Visualization
# =================================================
st.markdown("## 📈 " + t("Price Outlook", "توقعات السعر"))

chart_data = pd.DataFrame({
    t("Type", "النوع"): [t("Current Price", "السعر الحالي"), t("AI Predicted Price", "السعر المتوقع")],
    t("Price", "السعر"): [
        area_data["Avg_Price"].values[0],
        predicted_price
    ]
})

fig = px.bar(
    chart_data,
    x=chart_data.columns[0],
    y=chart_data.columns[1],
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# =================================================
# AI Insight
# =================================================
st.markdown("## 🧠 " + t("AI Insight", "رؤية الذكاء الاصطناعي"))
st.info(t(
    f"The AI model forecasts an average price of {int(predicted_price)} SAR/m² "
    f"in {selected_area}. Recommendation: {recommendation}.",
    f"يتوقع نموذج الذكاء الاصطناعي سعرًا متوسطه {int(predicted_price)} ريال/م² "
    f"في {selected_area}. التوصية: {recommendation}."
))

# =================================================
# AI CHAT ASSISTANT
# =================================================
st.markdown("## 💬 " + t("AI Investment Assistant", "مساعد استثماري ذكي"))

user_question = st.text_input(
    t("Ask SmartProp AI about this market...", "اسألي SmartProp AI عن هذا السوق...")
)

def ai_chat_response(question):
    demand = area_data["Demand_Index"].values[0]
    risk = area_data["Risk_Score"].values[0]
    current_price = area_data["Avg_Price"].values[0]

    if "why" in question.lower() or "ليش" in question:
        return t(
            f"The decision is based on demand ({demand}) and risk ({risk}).",
            f"القرار مبني على الطلب ({demand}) والمخاطرة ({risk})."
        )

    if "invest" in question.lower() or "استثمار" in question:
        return t(
            f"{selected_area} shows a predicted price of {int(predicted_price)} SAR/m² "
            f"vs current {current_price}. Recommendation: {recommendation}.",
            f"{selected_area} يظهر سعرًا متوقعًا {int(predicted_price)} ريال/م² "
            f"مقارنة بالحالي {current_price}. التوصية: {recommendation}."
        )

    return t(
        "This insight is generated using AI-driven demand and risk analysis.",
        "هذه الرؤية ناتجة عن تحليل الذكاء الاصطناعي للطلب والمخاطرة."
    )

if user_question:
    with st.spinner(t("SmartProp AI is thinking...", "SmartProp AI يفكر...")):
        st.success(ai_chat_response(user_question))

# =================================================
# CTA
# =================================================
st.markdown("---")
st.markdown("## 🚀 " + t(
    "Ready for full AI-powered market access?",
    "جاهزة للوصول الكامل لذكاء السوق؟"
))
st.button(t("Book a Free Demo", "احجزي عرضًا تجريبيًا مجانيًا"))
