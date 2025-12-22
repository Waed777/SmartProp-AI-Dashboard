# =================================================
# SmartProp AI - Global Creative Investment Platform
# =================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="SmartProp AI",
    page_icon="🏙️",
    layout="wide"
)

# =================================================
# LANGUAGE ENGINE
# =================================================
def t(en, ar):
    return en if st.session_state.language == "EN" else ar

if "language" not in st.session_state:
    st.session_state.language = "AR"

col1, col2 = st.columns([7,1])
with col2:
    if st.button("🌐 EN / AR"):
        st.session_state.language = "EN" if st.session_state.language == "AR" else "AR"

# =================================================
# BRANDING
# =================================================
st.markdown(t(
    "# 🏙️ SmartProp AI\n### Global AI Investment Assistant",
    "# 🏙️ SmartProp AI\n### منصة الذكاء الاستثماري العالمية"
))

st.markdown(t(
    "Ask SmartProp AI about this market",
    "اسألي SmartProp AI عن هذا السوق"
))

# =================================================
# USER PROFILE
# =================================================
st.sidebar.markdown(t("## Investor Profile", "## ملف المستثمر"))

budget = st.sidebar.selectbox(
    t("Budget", "الميزانية"),
    ["< 500K", "500K - 1M", "1M - 3M", "3M+"]
)

risk_tolerance = st.sidebar.selectbox(
    t("Risk Tolerance", "تحمل المخاطر"),
    ["Low", "Medium", "High"]
)

investment_goal = st.sidebar.selectbox(
    t("Goal", "الهدف"),
    ["Short Term", "Long Term", "Rental Income"]
)

user_profile = {
    "budget": budget,
    "risk": risk_tolerance,
    "goal": investment_goal
}

# =================================================
# MARKET DATA (Mock – Replace Later)
# =================================================
area_data = pd.DataFrame({
    "Area": ["North Riyadh"],
    "Demand_Index": [78],
    "Risk_Score": [42],
    "Avg_Price": [5100]
})

selected_area = area_data["Area"][0]
predicted_price = 5900
recommendation = "Buy"

# =================================================
# CHAT MEMORY
# =================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =================================================
# AI CHAT CORE (Extended from Old Code)
# =================================================
def ai_chat_response(
    question,
    area_data,
    predicted_price,
    recommendation,
    user_profile
):
    demand = area_data["Demand_Index"].values[0]
    risk = area_data["Risk_Score"].values[0]
    current_price = area_data["Avg_Price"].values[0]

    q = question.lower()

    # WHY
    if "why" in q or "ليش" in q or "لماذا" in q:
        return t(
            f"""
            📌 Recommendation Logic:
            - Demand Index: {demand}
            - Risk Score: {risk}
            - User Risk Preference: {user_profile['risk']}

            High demand with acceptable risk supports this recommendation.
            """,
            f"""
            📌 منطق التوصية:
            - مؤشر الطلب: {demand}
            - المخاطرة: {risk}
            - تحمل المستخدم للمخاطر: {user_profile['risk']}

            الطلب المرتفع مع مخاطرة مقبولة يدعم هذه التوصية.
            """
        )

    # IS IT GOOD INVESTMENT
    if any(word in q for word in ["good", "استثمار", "مناسب", "شراء"]):
        return t(
            f"""
            📊 Investment Insight:
            - Area: {selected_area}
            - Current Price: {current_price} SAR/m²
            - Predicted Price: {predicted_price} SAR/m²
            - AI Recommendation: {recommendation}

            Based on AI models, this area aligns with your investment profile.
            """,
            f"""
            📊 تحليل استثماري:
            - المنطقة: {selected_area}
            - السعر الحالي: {current_price} ريال/م²
            - السعر المتوقع: {predicted_price} ريال/م²
            - توصية الذكاء الاصطناعي: {recommendation}

            التحليل يتوافق مع ملفك الاستثماري.
            """
        )

    # COMPARE
    if "compare" in q or "قارن" in q or "مقارنة" in q:
        return t(
            "📈 Area comparison is available in the Enterprise version.",
            "📈 المقارنة بين المناطق متاحة في نسخة الشركات."
        )

    # FORECAST
    if "future" in q or "توقع" in q or "مستقبل" in q:
        growth = ((predicted_price - current_price) / current_price) * 100
        return t(
            f"Expected growth is approximately {growth:.1f}% over the next period.",
            f"النمو المتوقع تقريبًا {growth:.1f}% خلال الفترة القادمة."
        )

    # DEFAULT
    return t(
        "This insight is generated using AI-driven demand, risk, and price models.",
        "هذه الرؤية مبنية على نماذج ذكاء اصطناعي للطلب والمخاطر والأسعار."
    )

# =================================================
# CHAT UI
# =================================================
user_question = st.text_input(
    t("Type your question here...", "اكتبي سؤالك هنا...")
)

if user_question:
    with st.spinner(t("SmartProp AI is thinking...", "SmartProp AI يفكر...")):
        answer = ai_chat_response(
            user_question,
            area_data,
            predicted_price,
            recommendation,
            user_profile
        )

        st.session_state.chat_history.append({
            "time": datetime.now().strftime("%H:%M"),
            "question": user_question,
            "answer": answer
        })

# =================================================
# CHAT HISTORY
# =================================================
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑‍💼 {chat['question']}**")
    st.success(chat["answer"])

# =================================================
# MARKET DASHBOARD
# =================================================
st.markdown(t("## 📈 Market Dashboard", "## 📈 لوحة السوق"))

c1, c2, c3 = st.columns(3)
c1.metric(t("Demand Index", "مؤشر الطلب"), area_data["Demand_Index"][0])
c2.metric(t("Risk Score", "مؤشر المخاطر"), area_data["Risk_Score"][0])
c3.metric(t("Predicted Price", "السعر المتوقع"), f"{predicted_price} SAR/m²")

# =================================================
# FOOTER
# =================================================
st.markdown("---")
st.markdown(t(
    "SmartProp AI © 2025 – Global Creative Investment Platform",
    "SmartProp AI © 2025 – منصة استثمارية إبداعية عالمية"
))
