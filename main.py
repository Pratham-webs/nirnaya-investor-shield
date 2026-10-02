import streamlit as st
import time
import json
import os
import re
import pandas as pd

JOURNAL_FILE = "nirnaya_journal.json"

# --- PAGE SETUP & RESPONSIVE GLASSMORPHISM CSS ---
st.set_page_config(
    page_title="Nirnaya - Investor Resilience Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Dark Neon Glassmorphism Theme */
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2e, #0b0f19);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .neon-text {
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(79, 172, 254, 0.15);
        color: #4FACFE;
        border: 1px solid rgba(79, 172, 254, 0.3);
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        color: #0b0f19 !important;
        font-weight: 700;
        border: none;
        padding: 0.65rem 1rem;
        transition: all 0.25s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(0, 242, 254, 0.35);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 7-LANGUAGE TRANSLATION REGISTRY ---
TRANSLATIONS = {
    "English": {
        "title": "🛡️ Nirnaya: Investor Resilience Shield",
        "tagline": "Pause. Stress-test. Avoid scams. Protect your hard-earned capital.",
        "nav_journal": "📝 Decision Journal",
        "nav_scanner": "🕵️ Scam & Message Scanner",
        "nav_sebi": "🔍 SEBI License Validator",
        "nav_simulator": "💥 Crash Stress Simulator",
        "nav_chatbot": "🤖 Fin-Buster Chatbot",
        "nav_analytics": "📊 Behavioral Vibe Check",
        "nav_wisdom": "💡 Legends' Wisdom",
        "cb_warning": "⚠️ CIRCUIT BREAKER ACTIVATED",
        "cb_text": "System locked for 1 hour to prevent impulsive revenge trading. Cool down.",
        "breathe_btn": "Start 30-Second Breathing Exercise",
        "breathe_done": "Cognitive reset complete. Logic restored.",
        "q_asset": "Asset / Stock / Index Name",
        "q_amount": "Capital Allocation (₹)",
        "q_reason": "Investment Thesis (Why this? Why right now?):",
        "q_horizon": "Holding Horizon",
        "btn_journal": "Lock & Log Decision",
        "journal_success": "✅ Decision logged safely into private local storage.",
        "scam_alert": "🚨 DECEPTIVE PHRASE DETECTED",
        "scam_msg": "Your reasoning matches vectors common in unverified pump-and-dump tips. SEBI advisors never guarantee returns.",
        "history_title": "Past Recorded Theses",
        "history_empty": "No decisions logged yet.",
        "scanner_title": "WhatsApp & Telegram Tip Evaluator",
        "scanner_desc": "Paste suspicious promotional tips or forwards to audit for fraudulent patterns.",
        "scanner_input": "Paste suspicious message payload here:",
        "scanner_btn": "Audit Message for Red Flags",
        "scanner_clean": "✅ No overt scam buzzwords detected. Always independently verify SEBI registration.",
        "scanner_risk": "⚠️ HIGH RISK FRAUD VECTOR: Matches classic unverified pump-and-dump schemes.",
        "sebi_title": "Finfluencer SEBI License Validator",
        "sebi_desc": "Verify whether a financial influencer or tip channel uses a genuine SEBI format.",
        "sebi_input": "Enter SEBI Registration Number (e.g., INH000001234 or INA000005678):",
        "sebi_btn": "Validate Registration Format",
        "sim_title": "Market Crash Stress Simulator",
        "sim_desc": "Experience what severe market downturns feel like before committing real money.",
        "sim_input": "Hypothetical Capital to Stress-Test (₹):",
        "sim_calc": "Simulate Portfolio Shock",
        "login_prompt": "Choose a Nickname to Initialize Safe Session",
        "login_btn": "Launch Resilience Terminal",
        "logout_btn": "🚪 Logout Safe Session"
    },
    "हिन्दी (Hindi)": {
        "title": "🛡️ निर्णय: निवेशक सुरक्षा शील्ड",
        "tagline": "रुकें। सोचें। घोटालों से बचें। अपनी मेहनत की पूंजी सुरक्षित रखें।",
        "nav_journal": "📝 निर्णय डायरी",
        "nav_scanner": "🕵️ स्कैम व मैसेज स्कैनर",
        "nav_sebi": "🔍 सेबी लाइसेंस सत्यापन",
        "nav_simulator": "💥 बाजार गिरावट सिम्युलेटर",
        "nav_chatbot": "🤖 वित्तीय चैटबॉट",
        "nav_analytics": "📊 व्यवहार विश्लेषण (Vibe Check)",
        "nav_wisdom": "💡 दिग्गजों का ज्ञान",
        "cb_warning": "⚠️ सर्किट ब्रेकर सक्रिय",
        "cb_text": "जल्दबाजी और नुकसान की भरपाई वाले ट्रेड रोकने के लिए 1 घंटे का लॉक लगाया गया है।",
        "breathe_btn": "30-सेकंड का माइंडफुलनेस व्यायाम शुरू करें",
        "breathe_done": "तनाव कम हुआ। समझदारी से निर्णय लें।",
        "q_asset": "शेयर अथवा संपत्ति का नाम",
        "q_amount": "निवेश राशि (₹)",
        "q_reason": "आपका इस निवेश के पीछे क्या तर्क है?:",
        "q_horizon": "निवेश अवधि",
        "btn_journal": "निर्णय सुरक्षित दर्ज करें",
        "journal_success": "✅ निर्णय आपकी निजी लोकल मेमोरी में सुरक्षित दर्ज हो चुका है।",
        "scam_alert": "🚨 धोखाधड़ी संकेत मिला",
        "scam_msg": "आपके विवरण में ऐसे शब्द हैं जो फर्जी सोशल मीडिया टिप्स में इस्तेमाल होते हैं।",
        "history_title": "पुराने निर्णयों का रिकॉर्ड",
        "history_empty": "अभी कोई निर्णय दर्ज नहीं है।",
        "scanner_title": "व्हाट्सएप / टेलीग्राम टिप परीक्षक",
        "scanner_desc": "किसी भी सोशल मीडिया टिप या मैसेज को यहां पेस्ट करके जोखिम जांचें।",
        "scanner_input": "संदेश यहां पेस्ट करें:",
        "scanner_btn": "संदेश का विश्लेषण करें",
        "scanner_clean": "✅ कोई स्पष्ट फर्जी शब्द नहीं मिला। फिर भी आधिकारिक सेबी पंजीकरण जांचें।",
        "scanner_risk": "⚠️ अति उच्च जोखिम चेतावनी: यह भ्रामक प्रचार जैसा प्रतीत होता है।",
        "sebi_title": "फिनफ्लुएंसर सेबी लाइसेंस सत्यापन",
        "sebi_desc": "जांचें कि क्या टिप देने वाले का लाइसेंस नंबर आधिकारिक सेबी प्रारूप के अनुरूप है।",
        "sebi_input": "सेबी पंजीकरण संख्या दर्ज करें:",
        "sebi_btn": "प्रारूप की जांच करें",
        "sim_title": "बाजार गिरावट सिम्युलेटर",
        "sim_desc": "असली पैसे लगाने से पहले समझें कि बाजार क्रैश होने पर क्या असर होगा।",
        "sim_input": "परीक्षण राशि दर्ज करें (₹):",
        "sim_calc": "गिरावट का प्रभाव देखें",
        "login_prompt": "सत्र शुरू करने के लिए अपना उपनाम चुनें",
        "login_btn": "टर्मिनल शुरू करें",
        "logout_btn": "🚪 सुरक्षित लॉगआउट"
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🛡️ ನಿರ್ಣಯ: ಹೂಡಿಕೆದಾರರ ರಕ್ಷಣಾ ಕವಚ",
        "tagline": "ವಿರಾಮ ನೀಡಿ. ಯೋಚಿಸಿ. ವಂಚನೆಗಳಿಂದ ಪಾರಾಗಿ. ಬಂಡವಾಳ ರಕ್ಷಿಸಿ.",
        "nav_journal": "📝 ನಿರ್ಧಾರದ ಡೈರಿ",
        "nav_scanner": "🕵️ ವಂಚನೆ ಸಂದೇಶ ತಪಾಸಕ",
        "nav_sebi": "🔍 ಸೆಬಿ ಪರವಾನಗಿ ತಪಾಸಣೆ",
        "nav_simulator": "💥 ಮಾರುಕಟ್ಟೆ ಕುಸಿತದ ಸಿಮ್ಯುಲೇಟರ್",
        "nav_chatbot": "🤖 ಜಾರ್ಗನ್ ಬಸ್ಟರ್ ಚಾಟ್‌ಬಾಟ್",
        "nav_analytics": "📊 ನಡವಳಿಕೆ ವಿಶ್ಲೇಷಣೆ",
        "nav_wisdom": "💡 ಹೂಡಿಕೆ ದಿಗ್ಗಜರ ನುಡಿ",
        "cb_warning": "⚠️ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಸಕ್ರಿಯವಾಗಿದೆ",
        "cb_text": "ಹಠಾತ್ ವಹಿವಾಟು ಹಾಗೂ ನಷ್ಟ-ಬೆನ್ನಟ್ಟುವಿಕೆಯನ್ನು ತಡೆಯಲು ಸಿಸ್ಟಮ್ 1 ಗಂಟೆ ಲಾಕ್ ಆಗಿದೆ.",
        "breathe_btn": "30-ಸೆಕೆಂಡುಗಳ ಉಸಿರಾಟದ ವ್ಯಾಯಾಮ ಪ್ರಾರಂಭಿಸಿ",
        "breathe_done": "ಮನಸ್ಸು ಶಾಂತವಾಗಿದೆ. ವಿವೇಕಯುತ ನಿರ್ಧಾರ ಕೈಗೊಳ್ಳಿ.",
        "q_asset": "ಷೇರು ಅಥವಾ ಸ್ವತ್ತಿನ ಹೆಸರು",
        "q_amount": "ಹೂಡಿಕೆ ಮಾಡಲಿರುವ ಮೊತ್ತ (₹)",
        "q_reason": "ನೀವು ಈ ನಿರ್ಧಾರವನ್ನು ಏಕೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಿ?:",
        "q_horizon": "ಹೂಡಿಕೆಯ ಅವಧಿ",
        "btn_journal": "ನಿರ್ಧಾರ ದಾಖಲಿಸಿ",
        "journal_success": "✅ ನಿಮ್ಮ ಖಾಸಗಿ ಡೈರಿಯಲ್ಲಿ ನಿರ್ಧಾರ ಸುರಕ್ಷಿತವಾಗಿ ದಾಖಲಾಗಿದೆ.",
        "scam_alert": "🚨 ಸಂಭಾವ್ಯ ವಂಚನೆಯ ಲಕ್ಷಣ",
        "scam_msg": "ನಿಮ್ಮ ವಿವರಣೆಯಲ್ಲಿ ವಂಚಕರು ಬಳಸುವ ಪದಗಳಿವೆ. ಸೆಬಿ ಮಾನ್ಯತೆ ಪಡೆದವರು ಎಂದಿಗೂ ಖಚಿತ ಲಾಭದ ಭರವಸೆ ನೀಡುವುದಿಲ್ಲ.",
        "history_title": "ಹಿಂದಿನ ನಿರ್ಧಾರಗಳ ಇತಿಹಾಸ",
        "history_empty": "ಇನ್ನೂ ಯಾವುದೇ ನಿರ್ಧಾರಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ.",
        "scanner_title": "ವಾಟ್ಸಾಪ್ / ಟೆಲಿಗ್ರಾಮ್ ಟಿಪ್ ಸ್ಕ್ಯಾನರ್",
        "scanner_desc": "ಲಾಭದ ಆಮಿಷವೊಡ್ಡುವ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ ಅಪಾಯಕಾರಿ ಸುಳಿವುಗಳನ್ನು ಗುರುತಿಸಿ.",
        "scanner_input": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ:",
        "scanner_btn": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "scanner_clean": "✅ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಅಪಾಯಕಾರಿ ಪದಗಳಿಲ್ಲ. ಆದರೆ ಸೆಬಿ ನೋಂದಣಿ ಪರಿಶೀಲಿಸಿ.",
        "scanner_risk": "⚠️ ಹೆಚ್ಚಿನ ಅಪಾಯದ ಎಚ್ಚರಿಕೆ: ಇದು ವಂಚನೆಯ ಸಂದೇಶದ ಲಕ್ಷಣಗಳನ್ನು ಹೊಂದಿದೆ.",
        "sebi_title": "ಸೆಬಿ ನೋಂದಣಿ ಸಂಖ್ಯೆ ತಪಾಸಕ",
        "sebi_desc": "ಸಲಹೆಗಾರರು ನೀಡಿದ ಸೆಬಿ ಸಂಖ್ಯೆ ಅಧಿಕೃತ ಮಾದರಿಯಲ್ಲಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ.",
        "sebi_input": "ಸೆಬಿ ನೋಂದಣಿ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ:",
        "sebi_btn": "ಸಂಖ್ಯೆ ಪರಿಶೀಲಿಸಿ",
        "sim_title": "ಮಾರುಕಟ್ಟೆ ಕುಸಿತದ ಸಿಮ್ಯುಲೇಟರ್",
        "sim_desc": "ನಿಜವಾದ ಹಣ ತೊಡಗಿಸುವ ಮುನ್ನ ಮಾರುಕಟ್ಟೆ ಇಳಿಕೆಯ ನಷ್ಟವನ್ನು ನೇರವಾಗಿ ಗ್ರಹಿಸಿ.",
        "sim_input": "ಪರೀಕ್ಷಾರ್ಥ ಹೂಡಿಕೆ ಮೊತ್ತ (₹):",
        "sim_calc": "ನಷ್ಟದ ಪರಿಣಾಮ ಲೆಕ್ಕಹಾಕಿ",
        "login_prompt": "ಪ್ರವೇಶಿಸಲು ನಿಮ್ಮ ಅಡ್ಡಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "login_btn": "ಟರ್ಮಿನಲ್ ಪ್ರವೇಶಿಸಿ",
        "logout_btn": "🚪 ಸುರಕ್ಷಿತವಾಗಿ ನಿರ್ಗಮಿಸಿ"
    },
    "తెలుగు (Telugu)": {
        "title": "🛡️ నిర్ణయ: ఇన్వెస్టర్ రక్షణ షీల్డ్",
        "tagline": "ఆగండి. ఆలోచించండి. మోసాల నుండి రక్షించుకోండి. పెట్టుబడిని కాపాడుకోండి.",
        "nav_journal": "📝 నిర్ణయ డైరీ",
        "nav_scanner": "🕵️ స్కామ్ చెకర్",
        "nav_sebi": "🔍 సెబీ లైసెన్స్ ధృవీకరణ",
        "nav_simulator": "💥 క్రాష్ సిమ్యులేటర్",
        "nav_chatbot": "🤖 ఫైనాన్స్ చాట్‌బాట్",
        "nav_analytics": "📊 ప్రవర్తన విశ్లేషణ",
        "nav_wisdom": "💡 మార్కెట్ దిగ్గజాల సూత్రాలు",
        "cb_warning": "⚠️ సర్క్యూట్ బ్రేకర్ యాక్టివేట్ అయింది",
        "cb_text": "తొందరపాటు నిర్ణయాలు నిరోధించడానికి సిస్టమ్ 1 గంట లాక్ చేయబడింది.",
        "breathe_btn": "30-సెకన్ల శ్వాస వ్యాయామం ప్రారంభించండి",
        "breathe_done": "శాంతించండి. ఆలోచించి నిర్ణయం తీసుకోండి.",
        "q_asset": "స్టాక్ లేదా ఆస్తి పేరు",
        "q_amount": "పెట్టుబడి మొత్తం (₹)",
        "q_reason": "మీరు ఈ నిర్ణయం ఎందుకు తీసుకుంటున్నారు?:",
        "q_horizon": "కాలపరిమితి",
        "btn_journal": "నమోదు చేయండి",
        "journal_success": "✅ మీ నిర్ణయం సురక్షితంగా నమోదయింది.",
        "scam_alert": "🚨 మోసపూరిత సంకేతం గుర్తించబడింది",
        "scam_msg": "మీ కారణంలో ప్రమాదకర పదాలున్నాయి. సెబీ నమోదిత నిపుణులు ఎప్పుడూ గ్యారెంటీ లాభాలు వాగ్దానం చేయరు.",
        "history_title": "గత నిర్ణయాలు",
        "history_empty": "ఇంకా ఏ నిర్ణయాలు నమోదు కాలేదు.",
        "scanner_title": "టిప్ స్కానర్",
        "scanner_desc": "వాట్సాప్ లేదా టెలిగ్రామ్ మెసేజ్‌లను ఇక్కడ తనిఖీ చేయండి.",
        "scanner_input": "మెసేజ్ ఇక్కడ పేస్ట్ చేయండి:",
        "scanner_btn": "విశ్లేషించండి",
        "scanner_clean": "✅ స్పష్టమైన ప్రమాద సంకేతాలు లేవు.",
        "scanner_risk": "⚠️ ప్రమాద హెచ్చరిక: ఇది నకిలీ ప్రచారంగా కనిపిస్తోంది.",
        "sebi_title": "సెబీ రిజిస్ట్రేషన్ చెకర్",
        "sebi_desc": "సలహాదారు అందించిన సెబీ నంబర్ సరైన ఫార్మాట్‌లో ఉందో లేదో చూడండి.",
        "sebi_input": "సెబీ నంబర్ నమోదు చేయండి:",
        "sebi_btn": "ధృవీకరించండి",
        "sim_title": "క్రాష్ సిమ్యులేటర్",
        "sim_desc": "మార్కెట్ పడిపోతే మీ పెట్టుబడి ఎలా మారుతుందో చూడండి.",
        "sim_input": "మొత్తం నమోదు చేయండి (₹):",
        "sim_calc": "ప్రభావాన్ని లెక్కించండి",
        "login_prompt": "ముందుకు సాగడానికి నిక్‌నేమ్ ఎంచుకోండి",
        "login_btn": "ప్రవేశించండి",
        "logout_btn": "🚪 లాగ్ అవుట్"
    },
    "தமிழ் (Tamil)": {
        "title": "🛡️ நிர்ணயா: முதலீட்டாளர் பாதுகாப்பு கவசம்",
        "tagline": "பொறுங்கள். சிந்தியுங்கள். மோசடிகளைத் தவிருங்கள்.",
        "nav_journal": "📝 முடிவு டைரி",
        "nav_scanner": "🕵️ மோசடி சரிபார்ப்பு",
        "nav_sebi": "🔍 செபி உரிமச் சரிபார்ப்பு",
        "nav_simulator": "💥 சந்தை சரிவு சிமுலேட்டர்",
        "nav_chatbot": "🤖 நிதி சாட்பாட்",
        "nav_analytics": "📊 நடத்தை பகுப்பாய்வு",
        "nav_wisdom": "💡 ஜாம்பவான்களின் வழிகாட்டல்",
        "cb_warning": "⚠️ சர்க்யூட் பிரேக்கர் இயக்கப்பட்டது",
        "cb_text": "பதற்றமான முடிவுகளைத் தடுக்க கணினி 1 மணிநேரம் பூட்டப்பட்டுள்ளது.",
        "breathe_btn": "30 வினாடி சுவாசப் பயிற்சி",
        "breathe_done": "மன அமைதி அடைந்தது. தெளிவாக முடிவெடுங்கள்.",
        "q_asset": "பங்கு அல்லது சொத்தின் பெயர்",
        "q_amount": "முதலீட்டுத் தொகை (₹)",
        "q_reason": "இந்த முடிவை ஏன் எடுக்கிறீர்கள்?:",
        "q_horizon": "முதலீட்டுக் காலம்",
        "btn_journal": "பதிவு செய்",
        "journal_success": "✅ முடிவு வெற்றிகரமாகப் பதிவு செய்யப்பட்டது.",
        "scam_alert": "🚨 மோசடி எச்சரிக்கை",
        "scam_msg": "இதில் சந்தேகத்திற்கிடமான சொற்கள் உள்ளன. செபி ஆலோசகர்கள் உத்தரவாத லாபம் தருவதில்லை.",
        "history_title": "முந்தைய முடிவுகள்",
        "history_empty": "முடிவுகள் எதுவும் பதிவு செய்யப்படவில்லை.",
        "scanner_title": "செய்தி ஸ்கேனர்",
        "scanner_desc": "சந்தேகத்திற்குரிய தகவல்களைச் சோதிக்கவும்.",
        "scanner_input": "செய்தியை இங்கே ஒட்டவும்:",
        "scanner_btn": "ஆராய்க",
        "scanner_clean": "✅ வெளிப்படையான மோசடிச் சொற்கள் இல்லை.",
        "scanner_risk": "⚠️ அதிக ஆபத்து எச்சரிக்கை: இது மோசடி போன்றது.",
        "sebi_title": "செபி பதிவு சரிபார்ப்பு",
        "sebi_desc": "செபி பதிவு எண் சரியான வடிவத்தில் உள்ளதா எனப் பார்க்கவும்.",
        "sebi_input": "செபி பதிவு எண்:",
        "sebi_btn": "சரிபார்க்கவும்",
        "sim_title": "சரிவு சிமுலேட்டர்",
        "sim_desc": "பணத்தை முதலீடு செய்யும் முன் இழப்பு அபாயத்தை உணருங்கள்.",
        "sim_input": "தொகையை உள்ளிடவும் (₹):",
        "sim_calc": "தாக்கத்தைக் கணக்கிடு",
        "login_prompt": "புனைப்பெயரைத் தேர்ந்தெடுக்கவும்",
        "login_btn": "தொடரவும்",
        "logout_btn": "🚪 வெளியேறு"
    },
    "मराठी (Marathi)": {
        "title": "🛡️ निर्णय: गुंतवणूकदार संरक्षण कवच",
        "tagline": "थांबा. विचार करा. फसवणूक टाळा. भांडवल वाचवा.",
        "nav_journal": "📝 निर्णय नोंदवही",
        "nav_scanner": "🕵️ फसवणूक तपासक",
        "nav_sebi": "🔍 सेबी परवाना पडताळणी",
        "nav_simulator": "💥 घसरण सिम्युलेटर",
        "nav_chatbot": "🤖 वित्तीय चॅटबॉट",
        "nav_analytics": "📊 वर्तणूक विश्लेषण",
        "nav_wisdom": "💡 दिग्गजांचे विचार",
        "cb_warning": "⚠️ सर्किट ब्रेकर सक्रिय",
        "cb_text": "घाईघाईत घेतलेले नुकसानकारक व्यवहार टाळण्यासाठी सिस्टीम 1 तास लॉक आहे.",
        "breathe_btn": "30 सेकंदांचा श्वसन व्यायाम सुरू करा",
        "breathe_done": "मन शांत झाले आहे. शांतपणे निर्णय घ्या.",
        "q_asset": "शेअर किंवा मालमत्तेचे नाव",
        "q_amount": "गुंतवणूक रक्कम (₹)",
        "q_reason": "तुम्ही हा निर्णय का घेत आहात?:",
        "q_horizon": "कालावधी",
        "btn_journal": "नोंद करा",
        "journal_success": "✅ निर्णय यशस्वीरीत्या नोंदवला गेला आहे.",
        "scam_alert": "🚨 फसवणुकीचा इशारा",
        "scam_msg": "तुमच्या उत्तरात संशयास्पद शब्द आहेत. सेबी नोंदणीकृत सल्लागार हमी परतावा देत नाहीत.",
        "history_title": "मागील निर्णय",
        "history_empty": "अद्याप कोणताही निर्णय नोंदवलेला नाही.",
        "scanner_title": "टिप स्कॅनर",
        "scanner_desc": "व्हॉट्सॲप किंवा टेलिग्राम संदेशांची सत्यता तपासा.",
        "scanner_input": "संदेश येथे पेस्ट करा:",
        "scanner_btn": "तपासा",
        "scanner_clean": "✅ कोणताही संशयास्पद शब्द आढळला नाही.",
        "scanner_risk": "⚠️ उच्च जोखीम इशारा: हा फसवणुकीचा प्रकार असू शकतो.",
        "sebi_title": "सेबी नोंदणी पडताळणी",
        "sebi_desc": "सल्लागाराचा सेबी क्रमांक अधिकृत रचनेनुसार आहे का ते तपासा.",
        "sebi_input": "सेबी नोंदणी क्रमांक टाका:",
        "sebi_btn": "पडताळणी करा",
        "sim_title": "बाजार घसरण सिम्युलेटर",
        "sim_desc": "गुंतवणूक करण्यापूर्वी बाजार घसरल्यास काय होईल ते पहा.",
        "sim_input": "रक्कम टाका (₹):",
        "sim_calc": "परिणाम तपासा",
        "login_prompt": "सुरू करण्यासाठी टोपणनाव प्रविष्ट करा",
        "login_btn": "सुरू करा",
        "logout_btn": "🚪 लॉगआउट"
    },
    "বাংলা (Bengali)": {
        "title": "🛡️ নির্ণয়: বিনিয়োগকারী সুরক্ষা কবচ",
        "tagline": "থামুন। ভাবুন। প্রতারণা এড়ান। মূলধন বাঁচান।",
        "nav_journal": "📝 সিদ্ধান্তের ডায়েরি",
        "nav_scanner": "🕵️ প্রতারণা পরীক্ষক",
        "nav_sebi": "🔍 সেবি লাইসেন্স যাচাইকরণ",
        "nav_simulator": "💥 পতন সিমুলেটর",
        "nav_chatbot": "🤖 ফিন্যান্স চ্যাটবট",
        "nav_analytics": "📊 আচরণ মূল্যায়ন",
        "nav_wisdom": "💡 অভিজ্ঞদের পরামর্শ",
        "cb_warning": "⚠️ সার্কিট ব্রেকার সক্রিয়",
        "cb_text": "তাড়াহুড়ো করে সিদ্ধান্ত নেওয়া আটকাতে সিস্টেম ১ ঘণ্টার জন্য লক করা হয়েছে।",
        "breathe_btn": "৩০ সেকেন্ডের শ্বাস-প্রশ্বাসের ব্যায়াম",
        "breathe_done": "মন শান্ত হয়েছে। ভেবেচিন্তে পদক্ষেপ নিন।",
        "q_asset": "শেয়ার বা সম্পদের নাম",
        "q_amount": "বিনিয়োগের পরিমাণ (₹)",
        "q_reason": "কেন এই সিদ্ধান্ত নিচ্ছেন?:",
        "q_horizon": "সময়কাল",
        "btn_journal": "সিদ্ধান্ত নথিভুক্ত করুন",
        "journal_success": "✅ সিদ্ধান্ত সফলভাবে সংরক্ষিত হয়েছে।",
        "scam_alert": "🚨 প্রতারণার সতর্কতা",
        "scam_msg": "আপনার ব্যাখ্যায় ঝুঁকিপূর্ণ শব্দ রয়েছে। সেবি নিবন্ধিত উপদেষ্টারা নিশ্চিত রিটার্ন প্রতিশ্রুতি দেন না।",
        "history_title": "পূর্ববর্তী সিদ্ধান্ত",
        "history_empty": "এখনও কোনও সিদ্ধান্ত নথিভুক্ত করা হয়নি।",
        "scanner_title": "টিপ স্ক্যানার",
        "scanner_desc": "সন্দেহজনক মেসেজ বা সামাজিক মাধ্যমের টিপ যাচাই করুন।",
        "scanner_input": "মেসেজটি এখানে পেস্ট করুন:",
        "scanner_btn": "বিশ্লেষণ করুন",
        "scanner_clean": "✅ কোনও প্রতারণামূলক শব্দ মেলেনি।",
        "scanner_risk": "⚠️ উচ্চ ঝুঁকি সতর্কতা: এই মেসেজটি প্রতারণামূলক হতে পারে।",
        "sebi_title": "সেবি লাইসেন্স যাচাইকারী",
        "sebi_desc": "উপদেষ্টার সেবি নম্বর বৈধ বিন্যাসে আছে কিনা পরীক্ষা করুন।",
        "sebi_input": "সেবি নম্বর লিখুন:",
        "sebi_btn": "যাচাই করুন",
        "sim_title": "বাজার পতন সিমুলেটর",
        "sim_desc": "টাকা লাগানোর আগে বাজার পতনের ঝুঁকি অনুভব করুন।",
        "sim_input": "বিনিয়োগের পরিমাণ লিখুন (₹):",
        "sim_calc": "প্রভাব দেখুন",
        "login_prompt": "শুরু করতে একটি ছদ্মনাম নির্বাচন করুন",
        "login_btn": "প্রবেশ করুন",
        "logout_btn": "🚪 লগ আউট"
    }
}

RED_FLAGS = [
    # English
    "guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", "risk-free", 
    "100%", "insider", "double", "jackpot", "pump", "crypto bot", "zero risk",
    # Hindi
    "गारंटी", "पक्का", "टेलीग्राम", "व्हाट्सएप", "दोगुना",
    # Kannada
    "ಖಚಿತ", "ಗ್ಯಾರಂಟಿ", "ಟೆಲಿಗ್ರಾಮ್", "ವಾಟ್ಸಾಪ್", "ಡಬಲ್",
    # Telugu
    "గ్యారెంటీ", "టెలిగ్రామ్", "వాట్సాప్", "డబుల్",
    # Tamil
    "உத்தரவாதம்", "டெலிகிராம்", "வாட்ஸ்அப்", "இரட்டிப்பு",
    # Marathi
    "हमी", "टेलिग्राम", "व्हॉट्सॲप", "दुप्पट",
    # Bengali
    "নিশ্চিত", "টেলিগ্রাম", "হোয়াটসঅ্যাপ", "দ্বিগুণ"
]

# --- LOCAL DATABASE HANDLERS (PRIVACY-BY-DESIGN) ---
def load_journal():
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_journal(data):
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_circuit_breaker(journal_data, username):
    user_trades = [t for t in journal_data if t.get("user") == username]
    if len(user_trades) >= 3:
        last_trade_time = user_trades[-1].get("timestamp", 0)
        # 3600 seconds = 1 hour cooling off
        if time.time() - last_trade_time < 3600:
            return True
    return False

def scan_for_red_flags(text):
    text_lower = text.lower()
    return [word for word in RED_FLAGS if word in text_lower]

# --- SESSION INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Sidebar Language Selector
selected_lang = st.sidebar.selectbox(
    "🌐 Select Language / ಭಾಷೆ / भाषा",
    list(TRANSLATIONS.keys())
)
ui = TRANSLATIONS[selected_lang]

# --- LOGIN GATE ---
if not st.session_state["logged_in"]:
    st.markdown("<div class='glass-card' style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
    st.markdown("<span class='badge'>SEBI & NSDL SANGYAN SPRINT</span>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='neon-text'>{ui['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #94a3b8; font-size: 1.1rem;'>{ui['tagline']}</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            avatar = st.selectbox("Avatar", ["🧑‍💻", "🚀", "💎", "🦍", "📈", "🛡️"])
        with col2:
            username = st.text_input(ui["login_prompt"], placeholder="e.g. RationalTrader_01")
        
        submit_login = st.form_submit_button(ui["login_btn"])
        if submit_login:
            if username.strip():
                st.session_state["logged_in"] = True
                st.session_state["username"] = username.strip()
                st.session_state["avatar"] = avatar
                st.rerun()
            else:
                st.error("Please enter a nickname to proceed.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- AUTHENTICATED USER INTERFACE ---
    with st.sidebar:
        st.markdown(f"### {st.session_state['avatar']} **{st.session_state['username']}**")
        st.caption("Resilience Terminal: Online")
        st.divider()
        nav_choice = st.radio(
            "Navigation Menu",
            [
                ui["nav_journal"], 
                ui["nav_scanner"], 
                ui["nav_sebi"],
                ui["nav_simulator"], 
                ui["nav_chatbot"], 
                ui["nav_analytics"], 
                ui["nav_wisdom"]
            ]
        )
        st.divider()
        if st.button(ui["logout_btn"]):
            st.session_state["logged_in"] = False
            st.rerun()

    journal_data = load_journal()

    # --- 1. DECISION JOURNAL & CIRCUIT BREAKER (TRACK D) ---
    if nav_choice == ui["nav_journal"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK D: BEHAVIOURAL RESILIENCE</span><h2>{ui['nav_journal']}</h2><p style='color:#94a3b8;'>Enforce intentional friction and thesis validation before committing capital.</p></div>", unsafe_allow_html=True)
        
        if check_circuit_breaker(journal_data, st.session_state["username"]):
            st.error(ui["cb_warning"])
            st.warning(ui["cb_text"])
            
            # FOMO 30-Second Breathing Reset
            st.write(f"### 🫁 {ui['breathe_btn']}")
            progress_bar = st.progress(0)
            if st.button("Start Cool Down Timer"):
                for i in range(100):
                    time.sleep(0.3)
                    progress_bar.progress(i + 1)
                st.success(ui["breathe_done"])
        else:
            with st.form("decision_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    asset = st.text_input(ui["q_asset"], placeholder="e.g. Nifty 50 Index / Tata Motors")
                with col_b:
                    amount = st.slider(ui["q_amount"], min_value=500, max_value=200000, step=500, value=5000)
                
                reason = st.text_area(ui["q_reason"], placeholder="Explain the fundamental or risk thesis. What is the plan if it drops 20%?", height=120)
                horizon = st.select_slider(ui["q_horizon"], options=["Intraday (High Risk)", "Weeks", "Months", "Years", "Multi-Decade"])
                
                submitted = st.form_submit_button(ui["btn_journal"])
                if submitted:
                    if asset.strip() and reason.strip():
                        flags = scan_for_red_flags(reason)
                        if flags:
                            st.error(ui["scam_alert"])
                            st.warning(f"{ui['scam_msg']}\n\n**Deceptive Keywords Detected:** `{', '.join(flags)}`")
                        else:
                            entry = {
                                "user": st.session_state["username"],
                                "asset": asset.strip(),
                                "amount": amount,
                                "reason": reason.strip(),
                                "horizon": horizon,
                                "timestamp": time.time(),
                                "time_str": time.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            journal_data.append(entry)
                            save_journal(journal_data)
                            st.success(ui["journal_success"])
                    else:
                        st.warning("All input fields are required to log an investment thesis.")

        st.divider()
        st.subheader(ui["history_title"])
        user_history = [t for t in journal_data if t.get("user") == st.session_state["username"]]
        if user_history:
            for item in reversed(user_history[-5:]):
                with st.expander(f"📌 {item.get('asset', 'Unknown')} - ₹{item.get('amount', 0):,} ({item.get('time_str', 'Logged')})"):
                    st.write(f"**Horizon:** `{item.get('horizon')}`")
                    st.markdown(f"**Thesis:** {item.get('reason')}")
        else:
            st.info(ui["history_empty"])

    # --- 2. WHATSAPP & TELEGRAM SCAM SCANNER (TRACK A & E) ---
    elif nav_choice == ui["nav_scanner"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK A & E: SCAM INTERCEPTION</span><h2>{ui['scanner_title']}</h2><p style='color:#94a3b8;'>{ui['scanner_desc']}</p></div>", unsafe_allow_html=True)
        
        msg_input = st.text_area(ui["scanner_input"], height=140, placeholder="e.g. Join VIP Telegram group for 100% guaranteed jackpot multibagger, double money in 7 days...")
        if st.button(ui["scanner_btn"]):
            if msg_input.strip():
                found = scan_for_red_flags(msg_input)
                if found:
                    st.error(ui["scanner_risk"])
                    st.markdown(f"> **Identified Risk Triggers:** `{', '.join(found)}`")
                    st.warning("💡 **SEBI Advisory Rule:** Legitimate registered entities are prohibited from guaranteeing returns or distributing unverified insider stock tips.")
                else:
                    st.success(ui["scanner_clean"])
            else:
                st.warning("Please paste a message payload to evaluate.")

    # --- 3. SEBI REGISTRATION VALIDATOR (TRACK A & E) ---
    elif nav_choice == ui["nav_sebi"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK A: REGULATORY VERIFICATION</span><h2>{ui['sebi_title']}</h2><p style='color:#94a3b8;'>{ui['sebi_desc']}</p></div>", unsafe_allow_html=True)
        
        sebi_num = st.text_input(ui["sebi_input"], placeholder="e.g. INH000001234 or INA000005678")
        if st.button(ui["sebi_btn"]):
            clean_num = sebi_num.upper().strip()
            if re.match(r'^INH\d{9}$', clean_num):
                st.success(f"✅ FORMAT VALID: **{clean_num}** adheres to the SEBI Research Analyst format.")
                st.info("Next Step: Always verify this exact registration code on the official SEBI directory (`sebi.gov.in`) before transferring any funds.")
            elif re.match(r'^INA\d{9}$', clean_num):
                st.success(f"✅ FORMAT VALID: **{clean_num}** adheres to the SEBI Investment Adviser format.")
                st.info("Next Step: Always cross-check the registered entity name with the official SEBI database.")
            else:
                st.error("🚨 INVALID SEBI FORMAT: Authentic Research Analysts use 'INH' followed by 9 digits. Investment Advisers use 'INA' followed by 9 digits.")
                st.warning("Unregistered entities claiming regulatory approval operate illegally. Never share capital with unverified tip-sellers.")

    # --- 4. DOWNSIDE STRESS SIMULATOR (TRACK C) ---
    elif nav_choice == ui["nav_simulator"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK C: RISK AWARENESS</span><h2>{ui['sim_title']}</h2><p style='color:#94a3b8;'>{ui['sim_desc']}</p></div>", unsafe_allow_html=True)
        
        sim_cap = st.slider(ui["sim_input"], min_value=1000, max_value=500000, step=1000, value=25000)
        if st.button(ui["sim_calc"]):
            st.write("#### Probable Drawdown Scenarios:")
            c1, c2, c3 = st.columns(3)
            with c1:
                loss_10 = sim_cap * 0.10
                st.metric("Routine Pullback (-10%)", f"₹{sim_cap - loss_10:,.0f}", f"-₹{loss_10:,.0f}")
                st.caption("Common volatility occurring multiple times a year.")
            with c2:
                loss_25 = sim_cap * 0.25
                st.metric("Cyclical Bear Phase (-25%)", f"₹{sim_cap - loss_25:,.0f}", f"-₹{loss_25:,.0f}")
                st.caption("Protracted correction lasting 1-2 years.")
            with c3:
                loss_50 = sim_cap * 0.50
                st.metric("Severe Crisis (-50%)", f"₹{sim_cap - loss_50:,.0f}", f"-₹{loss_50:,.0f}")
                st.caption("Historic panics (e.g. 2008 GFC, March 2020 crash).")
            
            st.divider()
            st.warning("🛑 **Capital Resilience Rule:** If suffering a -₹{:,.0f} loss would impair daily household expenses or emergency liquidity, do not invest this capital in high-risk equity instruments.".format(loss_25))

    # --- 5. FIN-BUSTER JARGON CHATBOT (TRACK C) ---
    elif nav_choice == ui["nav_chatbot"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK C: INVESTOR EDUCATION</span><h2>{ui['nav_chatbot']}</h2><p style='color:#94a3b8;'>Deconstruct confusing financial terms using everyday analogies.</p></div>", unsafe_allow_html=True)
        
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                {"role": "assistant", "content": "Ask me to explain any financial term (e.g. NAV, F&O, Volatility, Compounding, Margin) in simple, relatable words."}
            ]
        
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if user_prompt := st.chat_input("Type a financial term..."):
            st.session_state["chat_history"].append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)
            
            p_low = user_prompt.lower()
            if "nav" in p_low:
                response = "**Net Asset Value (NAV):** Think of a mutual fund like a fruit basket. The NAV is simply the market price of one single scoop from that basket on a given day."
            elif "f&o" in p_low or "future" in p_low or "option" in p_low:
                response = "**Futures & Options (F&O):** 9 out of 10 individual traders lose money here. It is like putting down a non-refundable deposit to book a wedding hall. If you cancel, your deposit is gone. F&O is an institutional hedging tool, not a lottery ticket."
            elif "volatility" in p_low:
                response = "**Volatility:** It's like riding a bus on a bumpy dirt road versus a paved highway. High volatility means sharp jolts up and down. The long-term destination may be solid, but the turbulence shakes out unprepared riders."
            elif "compounding" in p_low:
                response = "**Compounding:** Think of planting a banyan tree sapling. In the early years, growth looks slow. Over decades, the branches drop aerial roots that become new trunks, multiplying shade exponentially."
            elif "margin" in p_low:
                response = "**Margin Trading:** Borrowing money from a broker to trade bigger volumes. If your trade works, gains multiply; if it drops even slightly, your collateral can be liquidated completely."
            else:
                response = f"**{user_prompt}** in simple terms: Never put capital into any instrument you cannot explain simply. If an advisor cannot explain the risk profile without jargon, protect your money by staying away."
            
            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

    # --- 6. VISUAL BEHAVIORAL ANALYTICS (TRACK D) ---
    elif nav_choice == ui["nav_analytics"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TRACK D: COGNITIVE PROFILING</span><h2>{ui['nav_analytics']}</h2><p style='color:#94a3b8;'>Algorithmic breakdown of your logged trading tendencies.</p></div>", unsafe_allow_html=True)
        
        user_history = [t for t in journal_data if t.get("user") == st.session_state["username"]]
        if not user_history:
            st.info("Log decisions in the Decision Journal to view your visual behavioral profile.")
        else:
            df = pd.DataFrame(user_history)
            total_decisions = len(user_history)
            short_term = sum(1 for t in user_history if "Intraday" in t.get("horizon", "") or "Weeks" in t.get("horizon", ""))
            total_capital = sum(t.get("amount", 0) for t in user_history)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Logged Decisions", total_decisions)
            col2.metric("Tracked Capital", f"₹{total_capital:,.0f}")
            col3.metric("Short-Term Focus", f"{int((short_term / total_decisions) * 100)}%")
            
            st.divider()
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                st.write("#### Capital Allocation by Asset")
                if "asset" in df.columns and "amount" in df.columns:
                    asset_grouped = df.groupby("asset")["amount"].sum()
                    st.bar_chart(asset_grouped, color="#4FACFE")
            
            with c_chart2:
                st.write("#### Holding Horizon Breakdown")
                if "horizon" in df.columns:
                    horizon_counts = df["horizon"].value_counts()
                    st.bar_chart(horizon_counts, color="#00F2FE")
            
            st.divider()
            st.subheader("Algorithmic Persona Diagnosis")
            if short_term > (total_decisions / 2) and total_decisions >= 3:
                st.error("🚨 **Persona: Impulsive Momentum Hunter**")
                st.markdown("> Your journal shows heavy concentration in short holding windows. This pattern strongly correlates with FOMO and emotional overtrading. Utilize the circuit breaker and expand your holding horizon.")
            elif total_decisions >= 3:
                st.success("🧘‍♂️ **Persona: Disciplined Wealth Compounder**")
                st.markdown("> Strong psychological resilience. Your recorded theses prioritize patient multi-month and multi-year time horizons, insulating you from daily volatility.")
            else:
                st.info(f"Recorded `{total_decisions}/3` entries. Complete 3 trade reflections to unlock your complete psychological profile.")

    # --- 7. LEGENDS' WISDOM (TRACK C & D) ---
    elif nav_choice == ui["nav_wisdom"]:
        st.markdown(f"<div class='glass-card'><span class='badge'>TIME-TESTED AWARENESS</span><h2>{ui['nav_wisdom']}</h2><p style='color:#94a3b8;'>Verified principles from market veterans to counter social media finfluencer hype.</p></div>", unsafe_allow_html=True)
        
        st.info("**Rakesh Jhunjhunwala:**\n\n*'Respect the market. Have an open mind. Know what to stake. Know when to take a loss. Be responsible.'*")
        st.success("**Warren Buffett:**\n\n*'The stock market is a device for transferring money from the impatient to the patient.'*")
        st.warning("**Peter Lynch:**\n\n*'Know what you own, and know why you own it.' (This is precisely why Nirnaya enforces documenting your thesis before buying).*")
        
        st.divider()
        st.markdown("> **Regulatory Guardrail Disclaimer:** Nirnaya is built strictly as public investor-protection infrastructure. It provides zero stock tips, buy/sell recommendations, price targets, or algorithmic trading funnels.")
