# ==========================================================
# AI SMART – REAL ESTATE DECISION ENGINE (CORE)
# This is NOT a dashboard. This is the brain.
# ==========================================================

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

# ----------------------------------------------------------
# 1. DATA MODEL
# ----------------------------------------------------------
# Expected columns:
# Area | Year | Demand_Index | Risk_Score | Avg_Price

class RealEstateAIEngine:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.model = None
        self.scaler = StandardScaler()
        self.features = ["Demand_Index", "Risk_Score", "Year"]
        self.target = "Avg_Price"

    # ------------------------------------------------------
    # 2. TRAIN MODEL (CORE INTELLIGENCE)
    # ------------------------------------------------------
    def train(self):
        X = self.data[self.features]
        y = self.data[self.target]

        self.model = Pipeline([
            ("scaler", self.scaler),
            ("regressor", LinearRegression())
        ])

        self.model.fit(X, y)
        return "AI Engine trained successfully"

    # ------------------------------------------------------
    # 3. PRICE FORECAST (FUTURE THINKING)
    # ------------------------------------------------------
    def forecast_price(self, area, year, demand, risk):
        input_df = pd.DataFrame([[demand, risk, year]], columns=self.features)
        prediction = self.model.predict(input_df)[0]
        return round(prediction, 2)

    # ------------------------------------------------------
    # 4. INVESTMENT SCORE (DECISION LOGIC)
    # ------------------------------------------------------
    def investment_score(self, demand, risk):
        score = (0.7 * demand) - (0.4 * risk)
        return round(score, 2)

    # ------------------------------------------------------
    # 5. RISK SIMULATION (MONTE CARLO LIGHT)
    # ------------------------------------------------------
    def risk_simulation(self, demand, risk, year, runs=500):
        results = []
        for _ in range(runs):
            d = np.random.normal(demand, 5)
            r = np.random.normal(risk, 5)
            price = self.forecast_price("X", year, d, r)
            results.append(price)

        return {
            "min": np.min(results),
            "max": np.max(results),
            "expected": np.mean(results)
        }

    # ------------------------------------------------------
    # 6. EXPLAINABILITY (WHY AI DECIDED THIS)
    # ------------------------------------------------------
    def explain_decision(self, demand, risk):
        explanation = []

        if demand > 75:
            explanation.append("High demand is driving price appreciation")
        else:
            explanation.append("Moderate demand limits upside")

        if risk > 60:
            explanation.append("Risk level is suppressing valuation")
        else:
            explanation.append("Risk is within acceptable investment range")

        return explanation

    # ------------------------------------------------------
    # 7. EXECUTIVE SUMMARY (INVESTOR LANGUAGE)
    # ------------------------------------------------------
    def executive_summary(self, area, year, demand, risk):
        price = self.forecast_price(area, year, demand, risk)
        score = self.investment_score(demand, risk)
        sim = self.risk_simulation(demand, risk, year)

        verdict = "STRONG OPPORTUNITY" if score > 40 else "CAUTION"

        return {
            "Area": area,
            "Year": year,
            "AI_Price": price,
            "Investment_Score": score,
            "Risk_Range": sim,
            "Verdict": verdict,
            "Narrative": self.explain_decision(demand, risk)
        }


# ----------------------------------------------------------
# 8. SAMPLE USAGE (THIS IS HOW BIG BOYS USE IT)
# ----------------------------------------------------------
if __name__ == "__main__":
    data = pd.DataFrame({
        "Area": ["North Riyadh"] * 6,
        "Year": [2020, 2021, 2022, 2023, 2024, 2025],
        "Demand_Index": [60, 65, 70, 80, 85, 90],
        "Risk_Score": [55, 50, 48, 45, 40, 35],
        "Avg_Price": [6200, 6500, 6900, 7600, 8200, 8800]
    })

    engine = RealEstateAIEngine(data)
    engine.train()

    report = engine.executive_summary(
        area="North Riyadh",
        year=2030,
        demand=95,
        risk=30
    )

    print("\nAI EXECUTIVE REPORT")
    for k, v in report.items():
        print(f"{k}: {v}")
