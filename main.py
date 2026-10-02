import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

# --- NEW: Red Flag Keywords ---
RED_FLAGS = [
    "guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", 
    "risk-free", "100%", "insider", "double", "jackpot",
    # Kannada red flags
    "ಖಚಿತ", "ಗ್ಯಾರಂಟಿ", "ಟೆಲಿಗ್ರಾಮ್", "ವಾಟ್ಸಾಪ್", "ಡಬಲ್" 
]

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

def scan_for_red_flags(reason_text):
    reason_lower = reason_text.lower()
    found_flags = [word for word in RED_FLAGS if word in reason_lower]
    return found_flags

# --- WEB INTERFACE (FRONTEND) ---
st.set_page_config(page_title="Nirnaya - Investor Shield")

# Language Toggle
lang = st.radio("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ (Kannada)"], horizontal=True)

if lang == "English":
    ui = {
        "title": "🛡️ Nirnaya: The Decision Journal",
        "sub": "Pause. Reflect. Protect your capital.",
        "cb_warning": "⚠️ CIRCUIT BREAKER ACTIVATED ⚠️",
        "cb_text": "System locked for 1 hour to prevent impulsive trading.",
        "q_asset": "What are you planning to invest in?",
        "q_reason": "Explain your reasoning (Be specific):",
        "q_horizon": "Is this for the short-term or long-term?",
        "btn": "Log Decision",
        "success": "✅ Decision logged successfully!",
        "warn": "Please fill out all fields to proceed.",
        "scam_alert": "🚨 POTENTIAL SCAM DETECTED 🚨",
        "scam_msg": "Your reasoning contains words often used by fraudsters. Remember: No legitimate advisor can offer 'guaranteed' returns or insider tips via social media. Please reconsider this trade."
    }
else:
    ui = {
        "title": "🛡️ ನಿರ್ಣಯ: ನಿರ್ಧಾರದ ಡೈರಿ",
        "sub": "ವಿರಾಮ. ಯೋಚಿಸಿ. ನಿಮ್ಮ ಬಂಡವಾಳವನ್ನು ರಕ್ಷಿಸಿ.",
        "cb_warning": "⚠️ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ ⚠️",
        "cb_text": "ಹಠಾತ್ ವಹಿವಾಟನ್ನು ತಡೆಯಲು ಸಿಸ್ಟಮ್ 1 ಗಂಟೆಯವರೆಗೆ ಲಾಕ್ ಆಗಿದೆ.",
        "q_asset": "ನೀವು ಯಾವುದರಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಲು ಯೋಚಿಸುತ್ತಿದ್ದೀರಿ?",
        "q_reason": "ನಿಮ್ಮ ಕಾರಣವನ್ನು ವಿವರಿಸಿ (ನಿಖರವಾಗಿರಲಿ):",
        "q_horizon": "ಇದು ಅಲ್ಪಾವಧಿ ಅಥವಾ ದೀರ್ಘಾವಧಿಗಾಗಿಯೇ?",
        "btn": "ನಿರ್ಧಾರವನ್ನು ದಾಖಲಿಸಿ",
        "success": "✅ ನಿರ್ಧಾರವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಿಸಲಾಗಿದೆ!",
        "warn": "ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಕ್ಷೇತ್ರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
        "scam_alert": "🚨 ಸಂಭಾವ್ಯ ವಂಚನೆ ಪತ್ತೆಯಾಗಿದೆ 🚨",
        "scam_msg": "ನಿಮ್ಮ ಕಾರಣದಲ್ಲಿ ವಂಚಕರು ಬಳಸುವ ಪದಗಳಿವೆ. ನೆನಪಿಡಿ: ಯಾವುದೇ ಕಾನೂನುಬದ್ಧ ಸಲಹೆಗಾರರು ಸಾಮಾಜಿಕ ಮಾಧ್ಯಮದ ಮೂಲಕ 'ಗ್ಯಾರಂಟಿ' ಆದಾಯವನ್ನು ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ."
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
        horizon = st.selectbox(ui["q_horizon"], ["Short-term / ಅಲ್ಪಾವಧಿ", "Long-term / ದೀರ್ಘಾವಧಿ"])
        
        submitted = st.form_submit_button(ui["btn"])
        
        if submitted:
            if asset and reason:
                # Run the security scan first
                flags = scan_for_red_flags(reason)
                
                if flags:
                    st.error(ui["scam_alert"])
                    st.warning(f"{ui['scam_msg']} \n\n**Flagged words detected:** {', '.join(flags)}")
                else:
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
