# =================================================
# IMPORTS (كودك + إضافات GPT)
# =================================================
import streamlit as st
import pandas as pd
import numpy as np
from openai import OpenAI


# =================================================
# OPENAI CLIENT
# =================================================
# حطي المفتاح في .streamlit/secrets.toml
# OPENAI_API_KEY="sk-xxxx"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# =================================================
# LANGUAGE HELPER (كما تستخدمينه)
# =================================================
def t(en, ar):
    return en if st.session_state.get("lang", "AR") == "EN" else ar


# =================================================
# SESSION STATE
# =================================================
if "lang" not in st.session_state:
    st.session_state.lang = "AR"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =================================================
# MOCK DATA (نفس فكرتك)
# =================================================
area_data = pd.DataFrame({
    "Area": ["North Riyadh"],
    "Demand_Index": [80],
    "Risk_Score": [40],
    "Avg_Price": [5200]
})

selected_area = "North Riyadh"
predicted_price = 6100
recommendation = "Strong Buy"


# =================================================
# UI (كودك كما هو)
# =================================================
st.markdown(t("## 💬 AI Investment Assistant", "## 💬 مساعد استثماري ذكي"))

st.markdown(t(
    "Ask SmartProp AI about this market",
    "اسألي SmartProp AI عن هذا السوق"
))

user_question = st.text_input(
    t("Type your question here...", "اكتبي سؤالك هنا...")
)


# =================================================
# ORIGINAL RULE-BASED FUNCTION (كودك 100%)
# =================================================
def ai_chat_response(question, area_data, predicted_price, recommendation):
    demand = area_data["Demand_Index"].values[0]
    risk = area_data["Risk_Score"].values[0]
    current_price = area_data["Avg_Price"].values[0]

    if "why" in question.lower() or "ليش" in question:
        return t(
            f"The recommendation is based on demand ({demand}) and risk ({risk}). "
            f"High demand with controlled risk supports this decision.",
            f"التوصية مبنية على مستوى الطلب ({demand}) والمخاطرة ({risk}). "
            f"الطلب المرتفع مع مخاطرة متحكم بها يدعم هذا القرار."
        )

    if "good" in question.lower() or "استثمار" in question:
        return t(
            f"Based on AI analysis, {selected_area} shows a predicted price of "
            f"{int(predicted_price)} SAR/m² compared to the current {current_price}. "
            f"This suggests: {recommendation}.",
            f"بناءً على تحليل الذكاء الاصطناعي، السعر المتوقع في {selected_area} هو "
            f"{int(predicted_price)} ريال/م² مقارنة بالسعر الحالي {current_price}. "
            f"وهذا يشير إلى: {recommendation}."
        )

    if "compare" in question.lower() or "قارن" in question:
        return t(
            "Comparison across areas is available in the Enterprise version.",
            "المقارنة بين المناطق متاحة في نسخة الشركات."
        )

    # 👇 مهم: لو ما عرف يجاوب
    return None


# =================================================
# GPT FALLBACK (إضافة فقط)
# =================================================
def gpt_response(question, area_data):
    context = f"""
    Area: {area_data['Area'].values[0]}
    Demand Index: {area_data['Demand_Index'].values[0]}
    Risk Score: {area_data['Risk_Score'].values[0]}
    Avg Price: {area_data['Avg_Price'].values[0]} SAR/m²
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional real estate investment AI assistant. Answer clearly and professionally."
            },
            {
                "role": "user",
                "content": context + "\n\nQuestion: " + question
            }
        ]
    )

    return completion.choices[0].message.content


# =================================================
# SMART WRAPPER (Rules → GPT)
# =================================================
def smart_ai_response(question):
    rule_answer = ai_chat_response(
        question,
        area_data,
        predicted_price,
        recommendation
    )

    if rule_answer is not None:
        return rule_answer

    return gpt_response(question, area_data)


# =================================================
# EXECUTION
# =================================================
if user_question:
    with st.spinner(t("SmartProp AI is thinking...", "SmartProp AI يفكر...")):
        answer = smart_ai_response(user_question)

        st.session_state.chat_history.append({
            "question": user_question,
            "answer": answer
        })

    st.success(answer)


# =================================================
# CHAT HISTORY
# =================================================
if st.session_state.chat_history:
    st.markdown(t("### 🧠 Chat History", "### 🧠 سجل المحادثة"))

    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑‍💼 {chat['question']}**")
        st.info(chat["answer"])
