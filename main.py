import streamlit as st
import time
import json
import os
import re
import pandas as pd

JOURNAL_FILE = "nirnaya_journal.json"

st.set_page_config(page_title="Nirnaya - Investor Resilience Shield", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1a1c2e, #0d0f18); color: #f1f5f9; }
    .glass-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
    .neon-text { background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; background: rgba(79, 172, 254, 0.15); color: #4FACFE; border: 1px solid rgba(79, 172, 254, 0.3); margin-bottom: 12px; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); color: #0b0f19 !important; font-weight: 700; border: none; transition: all 0.2s; }
    .stButton>button:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

RED_FLAGS = ["guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", "risk-free", "100%", "insider", "jackpot"]

# --- DATA FUNCTIONS ---
def load_journal():
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_journal(data):
    with open(JOURNAL_FILE, "w") as f: json.dump(data, f, indent=4)

def check_circuit_breaker(journal_data, username):
    user_trades = [t for t in journal_data if t.get("user") == username]
    if len(user_trades) >= 3:
        last_trade_time = user_trades[-1].get("timestamp", 0)
        if time.time() - last_trade_time < 3600: return True
    return False

# --- SESSION AUTHENTICATION ---
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<div class='glass-card' style='text-align: center; margin-top: 50px;'><span class='badge'>SANGYAN SPRINT</span><h1 class='neon-text'>🛡️ Nirnaya</h1><p>Initialize Safe Session.</p></div>", unsafe_allow_html=True)
    with st.form("login"):
        username = st.text_input("Nickname", placeholder="e.g. DiamondHands")
        if st.form_submit_button("Enter Terminal") and username.strip():
            st.session_state["logged_in"], st.session_state["username"] = True, username.strip()
            st.rerun()
else:
    with st.sidebar:
        st.markdown(f"### 🧑‍💻 **{st.session_state['username']}**")
        nav_choice = st.radio("Menu", ["📝 The Journal", "🕵️ Scam & SEBI Checker", "📊 Visual Analytics", "🤖 Fin-Buster Bot", "💥 Simulator"])
        if st.button("Logout"): st.session_state["logged_in"] = False; st.rerun()

    journal_data = load_journal()

    # --- 1. DECISION JOURNAL & FOMO PAUSE ---
    if nav_choice == "📝 The Journal":
        st.markdown("<div class='glass-card'><h2>Decision Journal</h2></div>", unsafe_allow_html=True)
        if check_circuit_breaker(journal_data, st.session_state["username"]):
            st.error("⚠️ FOMO CIRCUIT BREAKER ACTIVATED")
            st.warning("You are trading too rapidly. Step away from the screen.")
            
            # Interactive Breathing Exercise
            st.write("### 🫁 Mandatory 30-Second Cool Down")
            progress_bar = st.progress(0)
            if st.button("Start Breathing Exercise"):
                for i in range(100):
                    time.sleep(0.3)
                    progress_bar.progress(i + 1)
                st.success("Cool down complete. Logic restored. The system will unlock in 1 hour.")
        else:
            with st.form("decision_form"):
                asset = st.text_input("Asset Name")
                amount = st.slider("Capital (₹)", 500, 100000, 5000)
                reason = st.text_area("Your Thesis")
                horizon = st.select_slider("Horizon", ["Intraday", "Weeks", "Months", "Years"])
                if st.form_submit_button("Log Decision") and asset and reason:
                    if any(word in reason.lower() for word in RED_FLAGS):
                        st.error("🚨 FRAUD VECTOR DETECTED IN REASONING.")
                    else:
                        journal_data.append({"user": st.session_state["username"], "asset": asset, "amount": amount, "reason": reason, "horizon": horizon, "timestamp": time.time(), "time_str": time.strftime("%Y-%m-%d %H:%M")})
                        save_journal(journal_data)
                        st.success("✅ Trade logged.")

    # --- 2. SEBI REGISTRATION VALIDATOR ---
    elif nav_choice == "🕵️ Scam & SEBI Checker":
        st.markdown("<div class='glass-card'><h2>Finfluencer Trust Validator</h2></div>", unsafe_allow_html=True)
        st.write("Does the Telegram channel or 'Advisor' claim to be SEBI registered? Verify their format here.")
        
        sebi_num = st.text_input("Enter SEBI Registration Number provided by the advisor:", placeholder="e.g. INH000001234")
        if st.button("Validate Format"):
            sebi_num = sebi_num.upper().strip()
            if re.match(r'^INH\d{9}$', sebi_num):
                st.success(f"✅ FORMAT VALID: **{sebi_num}** matches the SEBI Research Analyst format.")
                st.info("Next Step: Manually search this exact number on `sebi.gov.in` to ensure they didn't steal a legitimate analyst's identity.")
            elif re.match(r'^INA\d{9}$', sebi_num):
                st.success(f"✅ FORMAT VALID: **{sebi_num}** matches the SEBI Investment Adviser format.")
            else:
                st.error("🚨 FORMAT INVALID: Genuine SEBI Research Analysts start with 'INH' followed by 9 digits. Investment Advisers start with 'INA' followed by 9 digits.")
                st.warning("If an advisor refuses to share an INH or INA number, they are operating illegally. Do not pay them.")

    # --- 3. VISUAL ANALYTICS DASHBOARD ---
    elif nav_choice == "📊 Visual Analytics":
        st.markdown("<div class='glass-card'><h2>Your Investment Vibe Check</h2></div>", unsafe_allow_html=True)
        user_history = [t for t in journal_data if t.get("user") == st.session_state["username"]]
        
        if not user_history:
            st.info("Log trades in the journal to view your visual behavior profile.")
        else:
            df = pd.DataFrame(user_history)
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Capital Allocation by Asset")
                asset_data = df.groupby("asset")["amount"].sum()
                st.bar_chart(asset_data, color="#4FACFE")
            
            with col2:
                st.write("### Trade Time Horizons")
                horizon_data = df["horizon"].value_counts()
                st.bar_chart(horizon_data, color="#00F2FE")

    # --- 4 & 5. CHATBOT & SIMULATOR ---
    elif nav_choice == "🤖 Fin-Buster Bot":
        st.write("### Ask about NAV, F&O, Margin, etc.")
        if prompt := st.chat_input("Type a term..."):
            st.chat_message("user").write(prompt)
            st.chat_message("assistant").write("I break down complex jargon. Remember, if you can't explain it to a 10-year-old, don't invest in it.")
            
    elif nav_choice == "💥 Simulator":
        st.write("### Downside Stress Test")
        sim_cap = st.slider("Test Capital (₹)", 1000, 500000, 25000)
        st.metric("25% Bear Market Drawdown", f"₹{sim_cap * 0.75:,.0f}", f"-₹{sim_cap * 0.25:,.0f}")
