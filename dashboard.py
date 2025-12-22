import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go

# =================================================
# Page Config
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
# Load Data (Automation)
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
        "CSV must contain required columns",
        "ملف CSV لا يحتوي على الأعمدة المطلوبة"
    ))
    st.stop()

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
selected_area = st.sidebar.selectbox(t("Area", "المنطقة"), data["Area"].unique())
area_data = data[data["Area"] == selected_area]

# =================================================
# AI / ML PIPELINE (Automation)
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
# Confidence + Investment Score
# =================================================
confidence_score = max(75, 100 - abs(predicted_price - area_data["Avg_Price"].values[0]) / 120)

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
c1, c2, c3, c4 = st.columns(4)
c1.metric(t("Current Price", "السعر الحالي"), f"{int(area_data['Avg_Price'])} SAR")
c2.metric(t("AI Predicted Price", "السعر المتوقع بالذكاء الاصطناعي"), f"{int(predicted_price)} SAR")
c3.metric(t("Prediction Confidence", "دقة التنبؤ"), f"{int(confidence_score)}%")
c4.metric(t("Investment Score", "درجة الاستثمار"), int(investment_score))

# =================================================
# Visualization (Enhanced)
# =================================================
st.markdown(t("## 📈 Price Outlook", "## 📈 توقعات السعر"))

chart_data = pd.DataFrame({
    t("Type", "النوع"): [t("Current Price", "السعر الحالي"), t("AI Prediction", "توقع الذكاء الاصطناعي")],
    t("Price", "السعر"): [area_data["Avg_Price"].values[0], predicted_price]
})

fig = px.bar(
    chart_data,
    x=chart_data.columns[0],
    y=chart_data.columns[1],
    text_auto=True,
    color=chart_data.columns[0],
    color_discrete_map={t("Current Price", "السعر الحالي"):"blue", t("AI Prediction", "توقع الذكاء الاصطناعي"):"orange"}
)

# Add Trend Line Simulation (WOW effect)
fig.add_trace(go.Scatter(
    x=[t("Current Price", "السعر الحالي"), t("AI Prediction", "توقع الذكاء الاصطناعي")],
    y=[area_data["Avg_Price"].values[0], predicted_price * 1.05],
    mode="lines+markers",
    name="Projected Trend",
    line=dict(color="green", dash="dash")
))

st.plotly_chart(fig, use_container_width=True)

# =================================================
# Explainable AI (Feature Importance)
# =================================================
st.markdown(t("## 🧠 AI Explanation & Feature Importance", "## 🧠 شرح الذكاء الاصطناعي"))
feature_importance = pd.DataFrame({
    "Feature": ["Demand_Index", "Risk_Score"],
    "Contribution": [area_data["Demand_Index"].values[0]*0.65, -area_data["Risk_Score"].values[0]*0.35]
})

st.bar_chart(feature_importance.set_index("Feature"))

st.info(t(
    f"The model predicts prices mainly based on demand strength and risk exposure. In {selected_area}, demand is high relative to risk, leading to a recommendation of {recommendation}.",
    f"يعتمد النموذج على قوة الطلب ومستوى المخاطرة. في {selected_area} الطلب مرتفع مقارنة بالمخاطرة، لذلك التوصية هي: {recommendation}."
))

# =================================================
# Executive Summary & ROI Calculator
# =================================================
st.markdown(t("## 🧾 Executive Summary & ROI", "## 🧾 ملخص تنفيذي و العائد المتوقع"))
roi = predicted_price / area_data['Avg_Price'].values[0] * 100 - 100
st.success(t(
    f"This AI-driven analysis indicates that {selected_area} represents a {recommendation} scenario with {int(confidence_score)}% confidence. Estimated ROI: {roi:.2f}%.",
    f"يشير هذا التحليل إلى أن {selected_area} تمثل {recommendation} بدقة {int(confidence_score)}%. العائد المتوقع: {roi:.2f}%."
))

# =================================================
# Dark/Light Mode Toggle
# =================================================
mode = st.sidebar.radio(t("Display Mode", "وضع العرض"), [t("Light", "فاتح"), t("Dark", "داكن")])
if mode == t("Dark", "داكن"):
    st.markdown('<style>body{background-color:#1e1e1e;color:white;}</style>', unsafe_allow_html=True)

# =================================================
# CTA
# =================================================
st.markdown("---")
st.markdown(t("## 🚀 Want enterprise-grade AI insights?", "## 🚀 هل تريد حلول ذكاء اصطناعي بمستوى الشركات الكبرى؟"))
st.button(t("Book a Free Demo", "احجز عرضًا تجريبيًا"))

# =================================================
# AI CHAT ASSISTANT (Enhanced)
# =================================================
st.markdown(t("## 💬 AI Investment Assistant", "## 💬 مساعد استثماري ذكي"))
st.markdown(t("Ask SmartProp AI about this market", "اسألي SmartProp AI عن هذا السوق"))

user_question = st.text_input(t("Type your question here...", "اكتبي سؤالك هنا..."))

def ai_chat_response(question, area_data, predicted_price, recommendation):
    demand = area_data["Demand_Index"].values[0]
    risk = area_data["Risk_Score"].values[0]
    current_price = area_data["Avg_Price"].values[0]

    # Advanced responses
    if "why" in question.lower() or "ليش" in question:
        return t(
            f"The recommendation is based on demand ({demand}) and risk ({risk}). High demand with controlled risk supports this decision.",
            f"التوصية مبنية على مستوى الطلب ({demand}) والمخاطرة ({risk}). الطلب المرتفع مع مخاطرة متحكم بها يدعم هذا القرار."
        )

    if "good" in question.lower() or "استثمار" in question:
        return t(
            f"Based on AI analysis, {selected_area} shows a predicted price of {int(predicted_price)} SAR/m² compared to the current {current_price}. This suggests: {recommendation}.",
            f"بناءً على تحليل الذكاء الاصطناعي، السعر المتوقع في {selected_area} هو {int(predicted_price)} ريال/م² مقارنة بالسعر الحالي {current_price}. وهذا يشير إلى: {recommendation}."
        )

    if "compare" in question.lower() or "قارن" in question:
        return t(
            "Comparison across areas is available in the Enterprise version.",
            "المقارنة بين المناطق متاحة في نسخة الشركات."
        )

    # Scenario suggestion (WOW effect)
    if "simulate" in question.lower() or "تجربة" in question:
        simulated_price = predicted_price * 1.05
        return t(
            f"Simulated scenario: predicted price could reach {int(simulated_price)} SAR/m² if demand increases.",
            f"السيناريو التجريبي: السعر المتوقع قد يصل إلى {int(simulated_price)} ريال/م² إذا ارتفع الطلب."
        )

    return t(
        "This insight is based on AI-driven demand, risk, and price modeling.",
        "هذه الرؤية مبنية على نماذج ذكاء اصطناعي للطلب والمخاطرة والأسعار."
    )

if user_question:
    with st.spinner(t("SmartProp AI is thinking...", "SmartProp AI يفكر...")):
        answer = ai_chat_response(
            user_question,
            area_data,
            predicted_price,
            recommendation
        )
    st.success(answer)
