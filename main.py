import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

def load_journal():
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as file:
            return json.load(file)
    return []

def save_journal(data):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(data, file, indent=4)

def check_circuit_breaker(journal_data):
    if len(journal_data) >= 3:
        last_trade_time = journal_data[-1]["timestamp"]
        current_time = time.time()
        
        if current_time - last_trade_time < 3600:
            return True
    return False

# --- WEB INTERFACE (FRONTEND) ---
st.set_page_config(page_title="Nirnaya - Investor Shield")

# Language Toggle
lang = st.radio("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ (Kannada)"], horizontal=True)

# Dictionary for UI text
if lang == "English":
    ui = {
        "title": "🛡️ Nirnaya: The Decision Journal",
        "sub": "Pause. Reflect. Protect your capital.",
        "cb_warning": "⚠️ CIRCUIT BREAKER ACTIVATED ⚠️",
        "cb_text": "You have made multiple rapid decisions. The system is locked for 1 hour to prevent impulsive trading.",
        "q_asset": "What are you planning to invest in?",
        "q_reason": "Take a deep breath. Explain your reasoning (Be specific):",
        "q_horizon": "Is this for the short-term or long-term?",
        "opt_short": "Short-term (days/weeks)",
        "opt_long": "Long-term (years)",
        "btn": "Log Decision",
        "success": "✅ Decision logged successfully! Review this in a week.",
        "warn": "Please fill out all fields to proceed."
    }
else:
    ui = {
        "title": "🛡️ ನಿರ್ಣಯ: ನಿರ್ಧಾರದ ಡೈರಿ",
        "sub": "ವಿರಾಮ. ಯೋಚಿಸಿ. ನಿಮ್ಮ ಬಂಡವಾಳವನ್ನು ರಕ್ಷಿಸಿ.",
        "cb_warning": "⚠️ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ ⚠️",
        "cb_text": "ನೀವು ವೇಗವಾಗಿ ಅನೇಕ ನಿರ್ಧಾರಗಳನ್ನು ಮಾಡಿದ್ದೀರಿ. ಹಠಾತ್ ವಹಿವಾಟನ್ನು ತಡೆಯಲು ಸಿಸ್ಟಮ್ 1 ಗಂಟೆಯವರೆಗೆ ಲಾಕ್ ಆಗಿದೆ.",
        "q_asset": "ನೀವು ಯಾವುದರಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಲು ಯೋಚಿಸುತ್ತಿದ್ದೀರಿ?",
        "q_reason": "ದೀರ್ಘವಾಗಿ ಉಸಿರಾಡಿ. ನಿಮ್ಮ ಕಾರಣವನ್ನು ವಿವರಿಸಿ (ನಿಖರವಾಗಿರಲಿ):",
        "q_horizon": "ಇದು ಅಲ್ಪಾವಧಿ ಅಥವಾ ದೀರ್ಘಾವಧಿಗಾಗಿಯೇ?",
        "opt_short": "ಅಲ್ಪಾವಧಿ (ದಿನಗಳು/ವಾರಗಳು)",
        "opt_long": "ದೀರ್ಘಾವಧಿ (ವರ್ಷಗಳು)",
        "btn": "ನಿರ್ಧಾರವನ್ನು ದಾಖಲಿಸಿ",
        "success": "✅ ನಿರ್ಧಾರವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಿಸಲಾಗಿದೆ!",
        "warn": "ಮುಂದುವರಿಯಲು ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ."
    }

st.title(ui["title"])
st.write(ui["sub"])

journal_data = load_journal()

if check_circuit_breaker(journal_data):
    st.error(ui["cb_warning"])
    st.write(ui["cb_text"])
else:
    with st.form("decision_form"):
        asset = st.text_input(ui["q_asset"])
        reason = st.text_area(ui["q_reason"])
        horizon = st.selectbox(ui["q_horizon"], [ui["opt_short"], ui["opt_long"]])
        
        submitted = st.form_submit_button(ui["btn"])
        
        if submitted:
            if asset and reason:
                entry = {
                    "asset": asset,
                    "reason": reason,
                    "horizon": horizon,
                    "timestamp": time.time()
                }
                journal_data.append(entry)
                save_journal(journal_data)
                st.success(ui["success"])
            else:
                st.warning(ui["warn"])