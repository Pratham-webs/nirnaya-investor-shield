import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

RED_FLAGS = [
    "guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", 
    "risk-free", "100%", "insider", "double", "jackpot", "pump",
    "ಖಚಿತ", "ಗ್ಯಾರಂಟಿ", "ಟೆಲಿಗ್ರಾಮ್", "ವಾಟ್ಸಾಪ್", "ಡಬಲ್" 
]

def load_journal():
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r") as file:
                return json.load(file)
        except Exception:
            return []
    return []

def save_journal(data):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(data, file, indent=4)

def check_circuit_breaker(journal_data):
    if len(journal_data) >= 3:
        last_trade_time = journal_data[-1].get("timestamp", 0)
        current_time = time.time()
        # 3600 seconds = 1 hour cooling off
        if current_time - last_trade_time < 3600:
            return True
    return False

def scan_for_red_flags(text):
    text_lower = text.lower()
    return [word for word in RED_FLAGS if word in text_lower]

st.set_page_config(page_title="Nirnaya - Investor Shield", page_icon="🛡️️", layout="centered")

# Language Selection
lang = st.radio("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ (Kannada)"], horizontal=True)

if lang == "English":
    ui = {
        "title": "🛡️ Nirnaya: Investor Resilience Shield",
        "sub": "Investor protection infrastructure for thoughtful decisions.",
        "tab1": "Decision Journal",
        "tab2": "Tip & Message Scanner",
        "cb_warning": "⚠️ CIRCUIT BREAKER ACTIVATED ⚠️",
        "cb_text": "System locked for 1 hour to prevent impulsive trading. Step back and reflect.",
        "q_asset": "What asset are you planning to enter?",
        "q_reason": "Explain your detailed reasoning (Why now? What is your thesis?):",
        "q_horizon": "Investment Horizon",
        "btn_journal": "Log Decision",
        "journal_success": "✅ Decision logged successfully.",
        "scam_alert": "🚨 RED FLAG DETECTED IN REASONING 🚨",
        "scam_msg": "Your entry contains phrases common in fraudulent promotions. Legitimate advisors do not promise guaranteed gains.",
        "history_title": "Your Past Reflections",
        "history_empty": "No decisions logged yet.",
        "scanner_title": "WhatsApp / Telegram Tip Checker",
        "scanner_desc": "Paste any message, tip, or post claiming quick financial gains to check for red flags.",
        "scanner_input": "Paste suspicious message here:",
        "scanner_btn": "Analyze Message",
        "scanner_clean": "✅ No common red-flag keywords detected. Still verify advisor SEBI registration before acting.",
        "scanner_risk": "⚠️️ HIGH RISK ALERT ⚠️ This message matches classic pump-and-dump patterns."
    }
else:
    ui = {
        "title": "🛡️ ನಿರ್ಣಯ: ಹೂಡಿಕೆದಾರರ ರಕ್ಷಣಾ ಕವಚ",
        "sub": "ವಿವೇಕಯುತ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ಹೂಡಿಕೆದಾರರ ಸಂರಕ್ಷಣಾ ವೇದಿಕೆ.",
        "tab1": "ನಿರ್ಧಾರದ ಡೈರಿ",
        "tab2": "ಸಂದೇಶ ತಪಾಸಕ",
        "cb_warning": "⚠️ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಸಕ್ರಿಯಗೊಳಿಸಲಾಗಿದೆ ⚠️",
        "cb_text": "ಹಠಾತ್ ವಹಿವಾಟು ತಡೆಯಲು ಸಿಸ್ಟಮ್ 1 ಗಂಟೆ ಲಾಕ್ ಆಗಿದೆ. ಸ್ವಲ್ಪ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ.",
        "q_asset": "ನೀವು ಯಾವ ಷೇರು/ಸ್ವತ್ತಿನಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡುತ್ತಿದ್ದೀರಿ?",
        "q_reason": "ನಿಮ್ಮ ಕಾರಣವನ್ನು ವಿವರವಾಗಿ ತಿಳಿಸಿ (ಏಕೆ ಈಗ? ನಿಮ್ಮ ಯೋಜನೆ ಏನು?):",
        "q_horizon": "ಹೂಡಿಕೆಯ ಅವಧಿ",
        "btn_journal": "ನಿರ್ಧಾರ ದಾಖಲಿಸಿ",
        "journal_success": "✅ ನಿರ್ಧಾರ ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ.",
        "scam_alert": "🚨 ಸಂಭಾವ್ಯ ವಂಚನೆಯ ಲಕ್ಷಣ ಪತ್ತೆಯಾಗಿದೆ 🚨",
        "scam_msg": "ನಿಮ್ಮ ವಿವರಣೆಯಲ್ಲಿ ವಂಚಕರು ಬಳಸುವ ಶಬ್ದಗಳಿವೆ. ಯಾವುದೇ ಮಾನ್ಯತೆ ಪಡೆದ ಸಲಹೆಗಾರರು ಖಚಿತ ಲಾಭದ ಭರವಸೆ ನೀಡುವುದಿಲ್ಲ.",
        "history_title": "ಹಿಂದಿನ ನಿರ್ಧಾರಗಳ ಇತಿಹಾಸ",
        "history_empty": "ಇನ್ನೂ ಯಾವುದೇ ನಿರ್ಧಾರಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ.",
        "scanner_title": "ವಾಟ್ಸಾಪ್ / ಟೆಲಿಗ್ರಾಮ್ ಸಂದೇಶ ತಪಾಸಣೆ",
        "scanner_desc": "ತ್ವರಿತ ಲಾಭದ ಭರವಸೆ ನೀಡುವ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ.",
        "scanner_input": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ:",
        "scanner_btn": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "scanner_clean": "✅ ಯಾವುದೇ ಅಪಾಯಕಾರಿ ಪದಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಆದರೂ ಸೆಬಿ (SEBI) ನೋಂದಣಿಯನ್ನು ದೃಢೀಕರಿಸಿ.",
        "scanner_risk": "⚠️ ಹೆಚ್ಚಿನ ಅಪಾಯದ ಎಚ್ಚರಿಕೆ ⚠️ ಈ ಸಂದೇಶವು ವಂಚನೆಯ ತಂತ್ರಗಳನ್ನು ಹೋಲುತ್ತದೆ."
    }

st.title(ui["title"])
st.caption(ui["sub"])

tab1, tab2 = st.tabs([ui["tab1"], ui["tab2"]])

# TAB 1: DECISION JOURNAL & CIRCUIT BREAKER
with tab1:
    journal_data = load_journal()
    
    if check_circuit_breaker(journal_data):
        st.error(ui["cb_warning"])
        st.write(ui["cb_text"])
    else:
        with st.form("decision_form"):
            asset = st.text_input(ui["q_asset"], placeholder="e.g. Tata Power / Nifty Index")
            reason = st.text_area(ui["q_reason"], placeholder="e.g. Fundamental growth prospects, 3-year target...")
            horizon = st.selectbox(ui["q_horizon"], ["Short-term / ಅಲ್ಪಾವಧಿ", "Long-term / ದೀರ್ಘಾವಧಿ"])
            
            submitted = st.form_submit_button(ui["btn_journal"])
            
            if submitted:
                if asset.strip() and reason.strip():
                    flags = scan_for_red_flags(reason)
                    if flags:
                        st.error(ui["scam_alert"])
                        st.warning(f"{ui['scam_msg']}\n\n**Flagged terms:** {', '.join(flags)}")
                    else:
                        entry = {
                            "asset": asset.strip(),
                            "reason": reason.strip(),
                            "horizon": horizon,
                            "timestamp": time.time(),
                            "time_str": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        journal_data.append(entry)
                        save_journal(journal_data)
                        st.success(ui["journal_success"])
                else:
                    st.warning("Please fill out both fields.")

    st.divider()
    st.subheader(ui["history_title"])
    if journal_data:
        for item in reversed(journal_data[-5:]):
            with st.expander(f"📌 {item.get('asset', 'Unknown')} ({item.get('time_str', 'Logged')})"):
                st.write(f"**Horizon:** {item.get('horizon')}")
                st.write(f"**Reasoning:** {item.get('reason')}")
    else:
        st.info(ui["history_empty"])

# TAB 2: WHATSAPP / TELEGRAM TIP CHECKER
with tab2:
    st.subheader(ui["scanner_title"])
    st.write(ui["scanner_desc"])
    
    msg_input = st.text_area(ui["scanner_input"], height=120, placeholder="e.g. Join VIP Telegram group for 100% sure-shot multibagger tips...")
    
    if st.button(ui["scanner_btn"]):
        if msg_input.strip():
            found = scan_for_red_flags(msg_input)
            if found:
                st.error(ui["scanner_risk"])
                st.markdown(f"> **Deceptive markers found:** `{', '.join(found)}`")
                st.info("💡 **Resilience Rule:** SEBI regulations strictly prohibit unregistered tip services from offering guaranteed returns.")
            else:
                st.success(ui["scanner_clean"])
        else:
            st.warning("Please enter a message to test.")