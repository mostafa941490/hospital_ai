import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
import traceback

# Local Imports
from model import load_model_and_scaler, predict_ml, generate_local_ai_insight, jarvis_chat_response_local
from database import init_db, save_patient, get_all_patients

try:
    # =========================
    # ⚙️ CONFIG & PAGE SETUP
    # =========================
    st.set_page_config(
        page_title="NEURAL HOSPITAL AI [FREE]",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize DB
    init_db()

    # ... وكل باقي الكود الأصلي حتى نهاية الملف ...

except Exception as e:
    st.error(f"🚨 Critical System Failure: {str(e)}")
    st.code(traceback.format_exc())
# Local Imports
from model import load_model_and_scaler, predict_ml, generate_local_ai_insight, jarvis_chat_response_local
from database import init_db, save_patient, get_all_patients

# =========================
# ⚙️ CONFIG & PAGE SETUP
# =========================
st.set_page_config(
    page_title="NEURAL HOSPITAL AI [FREE]",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize DB
init_db()

# =========================
# 🌍 STATE MANAGEMENT
# =========================
if 'lang' not in st.session_state:
    st.session_state.lang = "EN"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def t(en, ar):
    return ar if st.session_state.lang == "AR" else en

# =========================
# 🎨 CSS DESIGN SYSTEM (NASA + JARVIS)
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* Global Reset */
    .stApp {
        background-color: #050a12;
        color: #e0e0e0;
        font-family: 'Orbitron', 'Cairo', sans-serif;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Background Animation Effect */
    .main-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 50%, #0b1120 0%, #050a12 100%);
        z-index: -1;
    }
    .grid-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(0, 242, 234, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 242, 234, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: -1;
        pointer-events: none;
    }

    /* Neon Containers */
    .neon-box {
        background: rgba(11, 17, 32, 0.8);
        border: 1px solid #00f2ea;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #00f2ea !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 242, 234, 0.5);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #0b1120 !important;
        color: #00f2ea !important;
        border: 1px solid #00f2ea !important;
        border-radius: 5px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00f2ea 0%, #007c78 100%) !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 242, 234, 0.8) !important;
    }

    /* Chat Interface */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #1e293b;
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
    }
    .msg-user {
        background: #1e293b;
        color: white;
        padding: 8px 12px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        width: fit-content;
        margin-left: auto;
    }
    .msg-jarvis {
        background: rgba(0, 242, 234, 0.1);
        color: #00f2ea;
        border: 1px solid #00f2ea;
        padding: 8px 12px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        width: fit-content;
    }
</style>
<div class="main-bg"></div>
<div class="grid-overlay"></div>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN SYSTEM
# =========================
def login_screen():
    st.markdown("<h1 style='text-align:center; margin-top:50px;'>🏥 NEURAL HOSPITAL AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00f2ea;'>SECURE ACCESS TERMINAL [LOCAL MODE]</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="neon-box">', unsafe_allow_html=True)
            
            username = st.text_input("👤 OPERATOR ID", placeholder="admin / doctor / nurse")
            password = st.text_input("🔑 ACCESS CODE", type="password")
            
            st.markdown("---")
            st.caption("🛡️ BIOMETRIC VERIFICATION PROTOCOLS")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("👁️ Face ID"):
                    with st.spinner("Scanning Retina..."):
                        time.sleep(1.5)
                        st.success("Identity Verified")
            with c2:
                if st.button("🎙️ Voice ID"):
                    with st.spinner("Analyzing Voice Print..."):
                        time.sleep(1.5)
                        st.success("Voice Matched")
            with c3:
                if st.button("🧬 DNA Seq"):
                    with st.spinner("Sequencing..."):
                        time.sleep(1.5)
                        st.success("Access Granted")

            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("🚀 INITIALIZE SESSION", use_container_width=True):
                USERS = {
                    "admin": "admin123",
                    "doctor": "doc123",
                    "nurse": "nurse123"
                }
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_role = username
                    st.rerun()
                else:
                    st.error("⛔ ACCESS DENIED: Invalid Credentials")

# =========================
# 🛰️ MAIN DASHBOARD
# =========================
def main_dashboard():
    # Sidebar Controls
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3843/3843187.png", width=60)
        st.markdown(f"<h3 style='color:#00f2ea;'>CMDR. {st.session_state.user_role.upper()}</h3>", unsafe_allow_html=True)
        st.divider()
        
        if st.button("🌍 Switch Language"):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
            st.rerun()
            
        if st.button("🔒 LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # Header
    st.markdown(f"<h1>{t('MISSION CONTROL', 'غرفة التحكم الرئيسية')}</h1>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        t("🩺 Patient Diagnosis", "🩺 تشخيص المريض"), 
        t("📊 Analytics Hub", "📊 مركز التحليلات"),
        t("🤖 JARVIS Chat", "🤖 محادثة جارفيس")
    ])

    # --- TAB 1: DIAGNOSIS ---
    with tab1:
        col_input, col_result = st.columns([1, 1])
        
        with col_input:
            st.markdown('<div class="neon-box">', unsafe_allow_html=True)
            st.subheader(t("Vital Signs Input", "إدخال العلامات الحيوية"))
            
            p_name = st.text_input(t("Patient Name", "اسم المريض"))
            c1, c2 = st.columns(2)
            with c1:
                p_age = st.number_input(t("Age", "العمر"), 1, 120, 30)
                p_glucose = st.number_input(t("Glucose (mg/dL)", "الجلوكوز"), 0, 400, 120)
                p_bp = st.number_input(t("Blood Pressure", "ضغط الدم"), 0, 200, 80)
            with c2:
                p_bmi = st.number_input(t("BMI", "مؤشر الكتلة"), 10.0, 60.0, 25.0)
                p_insulin = st.number_input(t("Insulin Level", "الأنسولين"), 0, 900, 80)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("🧪 RUN AI DIAGNOSTIC", use_container_width=True):
                if p_name:
                    # 1. ML Prediction
                    model, scaler = load_model_and_scaler()
                    # Note: Aligning with Pima dataset structure roughly for demo
                    features = np.array([0, p_glucose, p_bp, 0, p_insulin, p_bmi, 0, p_age]) 
                    
                    pred, score, risk, color = predict_ml(model, scaler, features)
                    
                    # 2. Local AI Insight (The Free Magic)
                    patient_data = {
                        'glucose': p_glucose, 'bp': p_bp, 'bmi': p_bmi, 
                        'insulin': p_insulin, 'age': p_age
                    }
                    with st.spinner("🛰️ JARVIS is analyzing biological patterns..."):
                        time.sleep(1.5) # Fake processing time for effect
                        ai_text = generate_local_ai_insight(patient_data, risk, score)
                    
                    # 3. Save to DB
                    save_patient(p_name, p_age, p_glucose, p_bp, p_bmi, p_insulin, score, risk, ai_text)
                    
                    # Store results in session state
                    st.session_state.last_result = {
                        'name': p_name, 'risk': risk, 'score': score, 
                        'color': color, 'ai_text': ai_text, 'features': features
                    }
                    st.rerun()
                else:
                    st.warning("Please enter patient name.")

        with col_result:
            if 'last_result' in st.session_state:
                res = st.session_state.last_result
                st.markdown(f'<div class="neon-box" style="border-color:{res["color"]}; box-shadow: 0 0 20px {res["color"]}44;">', unsafe_allow_html=True)
                
                st.markdown(f"""
                <h2 style="color:{res['color']}; text-align:center;">{res['risk']}</h2>
                <h3 style="text-align:center;">CONFIDENCE: {res['score']:.1f}%</h3>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                labels = ['Glucose', 'BP', 'BMI', 'Insulin', 'Age']
                values_norm = [
                    res['features'][1]/4, # Glucose
                    res['features'][2]/2, # BP
                    res['features'][5],   # BMI
                    res['features'][4]/10,# Insulin
                    res['features'][7]/2  # Age
                ]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=values_norm,
                    theta=labels,
                    fill='toself',
                    fillcolor=res['color'],
                    line=dict(color=res['color'])
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=False)),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"**🤖 JARVIS ANALYSIS:**\n\n{res['ai_text']}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: ANALYTICS ---
    with tab2:
        st.subheader(t("Hospital Data Overview", "نظرة عامة على بيانات المستشفى"))
        df = get_all_patients()
        
        if not df.empty:
            k1, k2, k3 = st.columns(3)
            k1.metric("Total Patients", len(df))
            k2.metric("High Risk Cases", len(df[df['risk_level'] == 'HIGH RISK']))
            k3.metric("Avg Glucose", f"{df['glucose'].mean():.1f}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.line_chart(df[['glucose', 'bp']], color=["#00f2ea", "#ff4b4b"])
            with c2:
                st.bar_chart(df['risk_level'].value_counts(), color="#39ff14")
                
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No patient data recorded yet.")

    # --- TAB 3: JARVIS CHAT ---
    with tab3:
        st.markdown('<div class="chat-container" id="chatbox">', unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history:
            role = msg['role']
            text = msg['content']
            if role == "user":
                st.markdown(f'<div class="msg-user">{text}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-jarvis">🤖 {text}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        user_prompt = st.chat_input("Ask JARVIS...")
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            
            with st.spinner("JARVIS is thinking..."):
                # Use Local Chatbot Function
                response = jarvis_chat_response_local(user_prompt)
            
            st.session_state.chat_history.append({"role": "jarvis", "content": response})
            st.rerun()

# =========================
# 🏃 MAIN EXECUTION
# =========================
if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_screen()
    else:
        main_dashboard()
