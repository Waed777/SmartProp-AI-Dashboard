import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# =================================================
# Page Config (MUST BE FIRST STREAMLIT COMMAND)
# =================================================
st.set_page_config(
    page_title="SmartProp AI | Global Real Estate Intelligence",
    layout="wide"
)

# =================================================
# Language Toggle
# =================================================
language = st.sidebar.selectbox("🌐 Language | اللغة", ["English", "العربية"])

def t(en, ar):
    return en if language == "English" else ar

# =================================================
# Sidebar – Upload
# =================================================
st.sidebar.header(t("📁 Upload Your Data", "📁 رفع البيانات"))
uploaded_file = st.sidebar.file_uploader(
    t("Upload CSV file", "ارفع ملف CSV"),
    type=["csv"]
)

st.sidebar.markdown(t(
"""
**Required Columns**
- Area
- Demand_Index
- Risk_Score
- Avg_Price
""",
"""
**الأعمدة المطلوبة**
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

# =================================================
# Validate Columns
# =================================================
required_columns = {"Area", "Demand_Index", "Risk_Score", "Avg_Price"}
if not required_columns.issubset(data.columns):
    st.error(t(
        "CSV must contain required columns",
        "ملف CSV لا يحتوي على الأعمدة المطلوبة"
    ))
    st.stop()

# =================================================
# Ensure Numeric Data
# =================================================
numeric_cols = ["Demand_Index", "Risk_Score", "Avg_Price"]
data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors="coerce")
data = data.dropna()

# =================================================
# Header
# =================================================
st.title(t(
    "📊 SmartProp AI – Global Real Estate Decision Engine",
    "📊 سمارت بروب AI – محرك قرارات عقارية ذكي"
))
st.subheader(t(
    "AI-powered predictions for executives & investors",
    "تنبؤات مدعومة بالذكاء الاصطناعي لصناع القرار"
))

# =================================================
# Area Selection
# =================================================
st.sidebar.header(t("📍 Select Area", "📍 اختر المنطقة"))
selected_area = st.sidebar.selectbox(
    t("Area", "المنطقة"),
    data["Area"].unique()
)

area_data = data[data["Area"] == selected_area]

# =================================================
# AI / ML Pipeline
# =================================================
X = data[["Demand_Index", "Risk_Score"]]
y = data["Avg_Price"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

pipeline.fit(X, y)

predicted_price = pipeline.predict(
    area_data[["Demand_Index", "Risk_Score"]]
)[0]

# =================================================
# Scores
# =================================================
actual_price = area_data["Avg_Price"].values[0]

confidence_score = max(
    70,
    100 - abs(predicted_price - actual_price) / actual_price * 100
)

investment_score = (
    area_data["Demand_Index"].values[0] * 0.65
    - area_data["Risk_Score"].values[0] * 0.35
)

if investment_score > 45:
    recommendation = t("🔥 Strong Buy", "🔥 فرصة استثمار قوية")
elif investment_score > 25:
    recommendation = t("⚠️ Monitor Closely", "⚠️ راقب بحذر")
else:
    recommendation = t("❌ High Risk", "❌ مخاطرة عالية")

# =================================================
# Market Summary
# =================================================
st.markdown(t("## 📌 Market Summary", "## 📌 ملخص السوق"))

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    t("Current Price", "السعر الحالي"),
    f"{int(actual_price)} SAR"
)
c2.metric(
    t("AI Predicted Price", "السعر المتوقع بالذكاء الاصطناعي"),
    f"{int(predicted_price)} SAR"
)
c3.metric(
    t("Prediction Confidence", "دقة التنبؤ"),
    f"{int(confidence_score)}%"
)
c4.metric(
    t("Investment Score", "درجة الاستثمار"),
    int(investment_score)
)

# =================================================
# Visualization
# =================================================
st.markdown(t("## 📈 Price Outlook", "## 📈 توقعات السعر"))

chart_data = pd.DataFrame({
    t("Type", "النوع"): [
        t("Current Price", "السعر الحالي"),
        t("AI Prediction", "توقع الذكاء الاصطناعي")
    ],
    t("Price", "السعر"): [
        actual_price,
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
# Explainable AI
# =================================================
st.markdown(t("## 🧠 AI Explanation", "## 🧠 شرح قرار الذكاء الاصطناعي"))
st.info(t(
    f"The model relies on demand and risk indicators. "
    f"In {selected_area}, demand outweighs risk, resulting in: {recommendation}.",
    f"يعتمد النموذج على مؤشرات الطلب والمخاطرة. "
    f"في {selected_area} الطلب أعلى من المخاطرة، لذلك التوصية هي: {recommendation}."
))

# =================================================
# Executive Summary
# =================================================
st.markdown(t("## 🧾 Executive Summary", "## 🧾 ملخص تنفيذي"))
st.success(t(
    f"{selected_area} represents a {recommendation} scenario "
    f"with {int(confidence_score)}% confidence.",
    f"تشير النتائج إلى أن {selected_area} تمثل {recommendation} "
    f"بدقة {int(confidence_score)}%."
))

# =================================================
# CTA
# =================================================
st.markdown("---")
st.markdown(t(
    "## 🚀 Want enterprise-grade AI insights?",
    "## 🚀 هل تريد حلول ذكاء اصطناعي بمستوى الشركات الكبرى؟"
))
st.button(t("Book a Free Demo", "احجز عرضًا تجريبيًا"))

# =================================================
# AI CHAT ASSISTANT
# =================================================
st.markdown(t("## 💬 AI Investment Assistant", "## 💬 مساعد استثماري ذكي"))

user_question = st.text_input(
    t("Ask about this market...", "اسأل عن هذا السوق...")
)

def ai_chat_response(question):
    demand = area_data["Demand_Index"].values[0]
    risk = area_data["Risk_Score"].values[0]
    q = question.lower()

    if "why" in q or "ليش" in q:
        return t(
            f"The recommendation is driven by demand ({demand}) versus risk ({risk}).",
            f"التوصية ناتجة عن الطلب ({demand}) مقارنة بالمخاطرة ({risk})."
        )

    if "invest" in q or "استثمار" in q:
        return t(
            f"The AI predicts {int(predicted_price)} SAR compared to "
            f"{int(actual_price)} SAR currently. {recommendation}.",
            f"السعر المتوقع {int(predicted_price)} ريال مقابل "
            f"{int(actual_price)} حاليًا. {recommendation}."
        )

    return t(
        "This analysis is based on AI-driven demand and risk modeling.",
        "هذا التحليل مبني على نماذج ذكاء اصطناعي للطلب والمخاطرة."
    )

if user_question:
    with st.spinner(t("SmartProp AI is thinking...", "SmartProp AI يفكر...")):
        st.success(ai_chat_response(user_question))

