import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
import pickle
import os
import streamlit as st

@st.cache_resource
def load_model_and_scaler():
    """Load trained model or train a new one if missing."""
    model_path = 'model.pkl'
    scaler_path = 'scaler.pkl'

    if os.path.exists(model_path) and os.path.exists(scaler_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler

    # Training Phase (Only runs once on first deployment)
    st.info("🧠 Initializing Neural Core... Training Models...")
    try:
        data = pd.read_csv('diabetes.csv')
    except FileNotFoundError:
        st.error("❌ diabetes.csv not found! Please ensure it is in the root directory.")
        st.stop()

    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    rf = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42)
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
    
    final_model = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb)],
        voting='soft'
    )
    final_model.fit(X_train_scaled, y_train)
    
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    return final_model, scaler

def predict_ml(model, scaler, features_array):
    """Predict risk using the ML model."""
    features_scaled = scaler.transform([features_array])
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    confidence = max(probabilities) * 100
    
    if prediction == 1:
        risk_level = "HIGH RISK"
        color = "#ff4b4b"
    else:
        risk_level = "LOW RISK"
        color = "#00f2ea"
        
    return int(prediction), float(confidence), risk_level, color

# ==========================================
# 🧠 LOCAL AI ENGINE (Free Replacement for OpenAI)
# ==========================================
def generate_local_ai_insight(patient_ dict, ml_risk: str, ml_score: float) -> str:
    """
    Generates a professional medical insight based on WHO standards and clinical rules.
    No API Key required.
    """
    insights = []
    glu = patient_data['glucose']
    bp = patient_data['bp']
    bmi = patient_data['bmi']
    age = patient_data['age']
    insulin = patient_data['insulin']

    # 1. Glucose Analysis
    if glu > 140:
        insights.append(f"⚠️ <b>Glucose Alert:</b> Level ({glu} mg/dL) is significantly above normal fasting limits (>126). Immediate dietary control recommended.")
    elif glu > 100:
        insights.append(f"⚡ <b>Pre-Diabetic Warning:</b> Glucose ({glu} mg/dL) indicates impaired fasting glucose. Monitor sugar intake.")
    else:
        insights.append(f"✅ <b>Glucose Stable:</b> Level ({glu} mg/dL) is within healthy range.")

    # 2. Blood Pressure Analysis
    if bp > 140:
        insights.append(f"🔴 <b>Hypertension Risk:</b> BP ({bp} mmHg) is high. This strains the cardiovascular system.")
    elif bp > 120:
        insights.append(f"🟡 <b>Elevated BP:</b> Monitor salt intake and stress levels.")

    # 3. BMI & Weight Analysis
    if bmi > 30:
        insights.append(f"⚖️ <b>Obesity Class I:</b> BMI ({bmi}) contributes to insulin resistance. A 5-10% weight loss can drastically improve outcomes.")
    elif bmi > 25:
        insights.append(f"⚖️ <b>Overweight:</b> BMI ({bmi}) is above ideal. Focus on cardio exercises.")

    # 4. Insulin Resistance Check
    if insulin > 85 and glu > 100:
        insights.append(f" <b>Insulin Resistance:</b> High insulin combined with elevated glucose suggests early-stage metabolic syndrome.")

    # 5. Final Verdict based on ML Risk
    if "HIGH" in ml_risk:
        conclusion = f"\n\n🏥 <b>JARVIS FINAL VERDICT:</b> The patient shows strong indicators of Diabetes Mellitus. Confidence: {ml_score:.1f}%. <br>Recommendation: Consult an endocrinologist immediately for HbA1c testing."
    else:
        conclusion = f"\n\n🛡️ <b>JARVIS FINAL VERDICT:</b> Patient status is currently stable. Confidence: {ml_score:.1f}%. <br>Recommendation: Maintain current lifestyle and perform annual checkups."

    return "<br>".join(insights) + conclusion

def jarvis_chat_response_local(user_message: str) -> str:
    """
    Simple keyword-based chatbot for basic medical queries without API.
    """
    msg = user_message.lower()
    
    if "hello" in msg or "hi" in msg:
        return "Greetings. I am JARVIS, your local medical assistant. How may I assist you today?"
    elif "diabetes" in msg:
        return "Diabetes is a chronic condition that affects how your body turns food into energy. High blood sugar over time can lead to serious health problems."
    elif "diet" in msg or "food" in msg:
        return "For diabetic patients, focus on non-starchy vegetables, whole grains, lean proteins, and healthy fats. Avoid sugary drinks and refined carbs."
    elif "exercise" in msg or "sport" in msg:
        return "Regular physical activity helps lower blood sugar and boosts sensitivity to insulin. Aim for at least 150 minutes of moderate aerobic activity a week."
    elif "risk" in msg:
        return "Risk factors include family history, obesity, high blood pressure, and age over 45. Regular screening is key."
    else:
        return "I am currently operating in Local Mode. For complex queries, please consult a specialist. I can help with diet, exercise, and general diabetes info."