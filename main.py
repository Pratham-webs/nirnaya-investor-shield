import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

# Multilingual Red Flags
RED_FLAGS = [
    # English
    "guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", 
    "risk-free", "100%", "insider", "double", "jackpot", "pump", "crypto bot",
    # Hindi
    "गारंटी", "पक्का", "टेलीग्राम", "व्हाट्सएप", "दोगುना",
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

TRANSLATIONS = {
    "English": {
        "title": "🛡️ Nirnaya: Investor Resilience Shield",
        "sub": "Pause. Stress-test. Avoid scams. Protect your hard-earned capital.",
        "tab1": "Decision Journal",
        "tab2": "Tip & Scam Checker",
        "tab3": "Crash Stress Simulator",
        "cb_warning": "⚠️ CIRCUIT BREAKER ACTIVATED ⚠️",
        "cb_text": "System locked for 1 hour to prevent impulsive decisions. Take a break.",
        "q_asset": "Asset / Stock Name",
        "q_amount": "Amount you plan to invest (₹)",
        "q_reason": "Why are you taking this decision right now? (Detailed thesis):",
        "q_horizon": "Investment Horizon",
        "btn_journal": "Log Decision",
        "journal_success": "✅ Decision logged successfully into your local journal.",
        "scam_alert": "🚨 RED FLAG DETECTED 🚨",
        "scam_msg": "Your reasoning matches deceptive patterns. Legitimate SEBI advisors never guarantee returns.",
        "history_title": "Past Reflections",
        "history_empty": "No decisions logged yet.",
        "scanner_title": "WhatsApp & Telegram Tip Scanner",
        "scanner_desc": "Paste suspicious promotional messages, stock tips, or claims to evaluate risk.",
        "scanner_input": "Paste message here:",
        "scanner_btn": "Evaluate Message",
        "scanner_clean": "✅ No overt scam keywords found. Still verify SEBI registration before acting.",
        "scanner_risk": "⚠️ HIGH RISK ALERT ⚠️ This message exhibits classic deceptive or pump-and-dump signals.",
        "sim_title": "Market Crash Stress Simulator",
        "sim_desc": "Experience what downside volatility feels like before entering the trade.",
        "sim_input": "Enter planned investment amount (₹):",
        "sim_calc": "Calculate Downside Impact"
    },
    "हिन्दी (Hindi)": {
        "title": "🛡️ निर्णय: निवेशक सुरक्षा शील्ड",
        "sub": "रुकें। सोचें। घोटालों से बचें। अपनी पूंजी सुरक्षित रखें।",
        "tab1": "निर्णय डायरी",
        "tab2": "स्कैम व टिप चेकर",
        "tab3": "क्रैश स्ट्रेस सिम्युलेटर",
        "cb_warning": "⚠️ सर्किट ब्रेकर सक्रिय ⚠️",
        "cb_text": "जल्दबाजी में लिए जाने वाले ट्रेड को रोकने के लिए सिस्टम 1 घंटे के लिए लॉक है।",
        "q_asset": "शेयर या संपत्ति का नाम",
        "q_amount": "निवेश की जाने वाली राशि (₹)",
        "q_reason": "आप यह निर्णय अभी क्यों ले रहे हैं? (विस्तार से बताएं):",
        "q_horizon": "निवेश अवधि",
        "btn_journal": "निर्णय दर्ज करें",
        "journal_success": "✅ निर्णय आपकी लोकल डायरी में सुरक्षित दर्ज हो गया है।",
        "scam_alert": "🚨 धोखाधड़ी का संकेत मिला 🚨",
        "scam_msg": "आपके कारण में भ्रामक शब्द हैं। सेबी पंजीकृत सलाहकार कभी निश्चित रिटर्न की गारंटी नहीं देते।",
        "history_title": "पुराने निर्णय",
        "history_empty": "अभी तक कोई निर्णय दर्ज नहीं किया गया।",
        "scanner_title": "व्हाट्सएप / टेलीग्राम टिप स्कैनर",
        "scanner_desc": "किसी भी संदिग्ध टिप या संदेश को यहां जांचें।",
        "scanner_input": "संदेश यहां पेस्ट करें:",
        "scanner_btn": "संदेश का विश्लेषण करें",
        "scanner_clean": "✅ कोई स्पष्ट जोखिम भरा शब्द नहीं मिला। फिर भी आधिकारिक सेबी पंजीकरण जांचें।",
        "scanner_risk": "⚠️ उच्च जोखिम चेतावनी ⚠️ यह संदेश संदिग्ध पंप-एंड-डंप जैसा दिखता है।",
        "sim_title": "बाजार गिरावट सिम्युलेटर",
        "sim_desc": "पैसे लगाने से पहले समझें कि बाजार गिरने पर कैसा असर होगा।",
        "sim_input": "नियोजित निवेश राशि दर्ज करें (₹):",
        "sim_calc": "नुकसान का प्रभाव देखें"
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🛡️ ನಿರ್ಣಯ: ಹೂಡಿಕೆದಾರರ ರಕ್ಷಣಾ ಕವಚ",
        "sub": "ವಿರಾಮ ನೀಡಿ. ಯೋಚಿಸಿ. ವಂಚನೆಗಳಿಂದ ಪಾರಾಗಿ. ಬಂಡವಾಳ ರಕ್ಷಿಸಿ.",
        "tab1": "ನಿರ್ಧಾರದ ಡೈರಿ",
        "tab2": "ಸಂದೇಶ ತಪಾಸಕ",
        "tab3": "ಮಾರುಕಟ್ಟೆ ಇಳಿಕೆ ಸಿಮ್ಯುಲೇಟರ್",
        "cb_warning": "⚠️ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಸಕ್ರಿಯವಾಗಿದೆ ⚠️",
        "cb_text": "ಹಠಾತ್ ವಹಿವಾಟು ತಪ್ಪಿಸಲು ಸಿಸ್ಟಮ್ 1 ಗಂಟೆ ಲಾಕ್ ಆಗಿದೆ.",
        "q_asset": "ಷೇರು ಅಥವಾ ಸ್ವತ್ತಿನ ಹೆಸರು",
        "q_amount": "ಹೂಡಿಕೆ ಮಾಡಲಿರುವ ಮೊತ್ತ (₹)",
        "q_reason": "ನೀವು ಈ ನಿರ್ಧಾರವನ್ನು ಏಕೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಿ? (ವಿವರಿಸಿ):",
        "q_horizon": "ಹೂಡಿಕೆಯ ಅವಧಿ",
        "btn_journal": "ನಿರ್ಧಾರ ದಾಖಲಿಸಿ",
        "journal_success": "✅ ನಿರ್ಧಾರ ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ.",
        "scam_alert": "🚨 ಸಂಭಾವ್ಯ ವಂಚನೆ ಎಚ್ಚರಿಕೆ 🚨",
        "scam_msg": "ನಿಮ್ಮ ವಿವರಣೆಯಲ್ಲಿ ವಂಚನೆಯ ಲಕ್ಷಣಗಳಿವೆ. ಸೆಬಿ ಮಾನ್ಯತೆ ಪಡೆದವರು ಎಂದಿಗೂ ಖಚಿತ ಲಾಭದ ಭರವಸೆ ನೀಡಲ್ಲ.",
        "history_title": "ಹಿಂದಿನ ನಿರ್ಧಾರಗಳು",
        "history_empty": "ಇನ್ನೂ ಯಾವುದೇ ನಿರ್ಧಾರಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ.",
        "scanner_title": "ವಾಟ್ಸಾಪ್ / ಟೆಲಿಗ್ರಾಮ್ ಟಿಪ್ ಸ್ಕ್ಯಾನರ್",
        "scanner_desc": "ಲಾಭದ ಆಮಿಷವೊಡ್ಡುವ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಪರೀಕ್ಷಿಸಿ.",
        "scanner_input": "ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ:",
        "scanner_btn": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "scanner_clean": "✅ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಅಪಾಯಕಾರಿ ಪದಗಳಿಲ್ಲ. ಆದರೆ ಸೆಬಿ ನೋಂದಣಿ ಪರಿಶೀಲಿಸಿ.",
        "scanner_risk": "⚠️ ಹೆಚ್ಚಿನ ಅಪಾಯದ ಎಚ್ಚರಿಕೆ ⚠️ ಇದು ವಂಚನೆಯ ಸಂದೇಶದಂತಿದೆ.",
        "sim_title": "ಮಾರುಕಟ್ಟೆ ಕುಸಿತದ ಸಿಮ್ಯುಲೇಟರ್",
        "sim_desc": "ನಿಜವಾದ ಹಣ ತೊಡಗಿಸುವ ಮುನ್ನ ಮಾರುಕಟ್ಟೆ ಇಳಿಕೆಯ ನಷ್ಟವನ್ನು ಗ್ರಹಿಸಿ.",
        "sim_input": "ಹೂಡಿಕೆ ಮೊತ್ತ ನಮೂದಿಸಿ (₹):",
        "sim_calc": "ನಷ್ಟದ ಪರಿಣಾಮ ಲೆಕ್ಕಹಾಕಿ"
    },
    "తెలుగు (Telugu)": {
        "title": "🛡️ నిర్ణయ: ఇన్వెస్టర్ రక్షణ షీల్డ్",
        "sub": "ఆగండి. ఆలోచించండి. మోసాల నుండి రక్షించుకోండి.",
        "tab1": "నిర్ణయ డైరీ",
        "tab2": "స్కామ్ చెకర్",
        "tab3": "మార్కెట్ క్రాష్ సిమ్యులేటర్",
        "cb_warning": "⚠️ సర్క్యూట్ బ్రేకర్ యాక్టివేట్ అయింది ⚠️",
        "cb_text": "తొందరపాటు నిర్ణయాలు నిరోధించడానికి సిస్టమ్ 1 గంట లాక్ చేయబడింది.",
        "q_asset": "షేర్ లేదా ఆస్తి పేరు",
        "q_amount": "పెట్టుబడి మొత్తం (₹)",
        "q_reason": "మీరు ఈ నిర్ణయం ఎందుకు తీసుకుంటున్నారు?:",
        "q_horizon": "కాలపరిమితి",
        "btn_journal": "నమోదు చేయండి",
        "journal_success": "✅ మీ నిర్ణయం సురక్షితంగా నమోదయింది.",
        "scam_alert": "🚨 మోసపూరిత సంకేతం 🚨",
        "scam_msg": "మీ కారణంలో ప్రమాదకర పదాలున్నాయి. సెబీ నమోదిత నిపుణులు ఎప్పుడూ గ్యారెంటీ లాభాలు వాగ్దానం చేయరు.",
        "history_title": "గత నిర్ణయాలు",
        "history_empty": "ఇంకా ఏ నిర్ణయాలు నమోదు కాలేదు.",
        "scanner_title": "టిప్ స్కానర్",
        "scanner_desc": "వాట్సాప్ లేదా టెలిగ్రామ్ మెసేజ్‌లను ఇక్కడ తనిఖీ చేయండి.",
        "scanner_input": "మెసేజ్ ఇక్కడ పేస్ట్ చేయండి:",
        "scanner_btn": "విశ్లేషించండి",
        "scanner_clean": "✅ స్పష్టమైన ప్రమాద సంకేతాలు లేవు.",
        "scanner_risk": "⚠️ ప్రమాద హెచ్చరిక ⚠️ ఇది మోసపూరిత ప్రచారంగా కనిపిస్తోంది.",
        "sim_title": "క్రాష్ సిమ్యులేటర్",
        "sim_desc": "మార్కెట్ పడిపోతే మీ పెట్టుబడి ఎలా మారుతుందో చూడండి.",
        "sim_input": "మొత్తం నమోదు చేయండి (₹):",
        "sim_calc": "ప్రభావాన్ని లెక్కించండి"
    },
    "தமிழ் (Tamil)": {
        "title": "🛡️ நிர்ணயா: முதலீட்டாளர் பாதுகாப்பு கவசம்",
        "sub": "பொறுங்கள். சிந்தியுங்கள். மோசடிகளைத் தவிருங்கள்.",
        "tab1": "முடிவு டைரி",
        "tab2": "மோசடி சரிபார்ப்பு",
        "tab3": "சந்தை சரிவு சிமுலேட்டர்",
        "cb_warning": "⚠️ சர்க்யூட் பிரேக்கர் இயக்கப்பட்டது ⚠️",
        "cb_text": "பதற்றமான முடிவுகளைத் தடுக்க கணினி 1 மணிநேரம் பூட்டப்பட்டுள்ளது.",
        "q_asset": "பங்கு அல்லது சொத்தின் பெயர்",
        "q_amount": "முதலீட்டுத் தொகை (₹)",
        "q_reason": "இந்த முடிவை ஏன் எடுக்கிறீர்கள்? (விளக்கவும்):",
        "q_horizon": "முதலீட்டுக் காலம்",
        "btn_journal": "பதிவு செய்",
        "journal_success": "✅ முடிவு வெற்றிகரமாகப் பதிவு செய்யப்பட்டது.",
        "scam_alert": "🚨 மோசடி எச்சரிக்கை 🚨",
        "scam_msg": "இதில் சந்தேகத்திற்கிடமான சொற்கள் உள்ளன. செபி ஆலோசகர்கள் உத்தரவாத லாபம் தருவதில்லை.",
        "history_title": "முந்தைய முடிவுகள்",
        "history_empty": "முடிவுகள் எதுவும் பதிவு செய்யப்படவில்லை.",
        "scanner_title": "செய்தி ஸ்கேனர்",
        "scanner_desc": "சந்தேகத்திற்குரிய வாட்ஸ்அப் தகவல்களைச் சோதிக்கவும்.",
        "scanner_input": "செய்தியை இங்கே ஒட்டவும்:",
        "scanner_btn": "ஆராய்க",
        "scanner_clean": "✅ வெளிப்படையான மோசடிச் சொற்கள் இல்லை.",
        "scanner_risk": "⚠️ அதிக ஆபத்து எச்சரிக்கை ⚠️ இது மோசடி போன்றது.",
        "sim_title": "சரிவு சிமுலேட்டர்",
        "sim_desc": "பணத்தை முதலீடு செய்யும் முன் இழப்பு அபாயத்தை உணருங்கள்.",
        "sim_input": "தொகையை உள்ளிடவும் (₹):",
        "sim_calc": "தாக்கத்தைக் கணக்கிடு"
    },
    "मराठी (Marathi)": {
        "title": "🛡️ निर्णय: गुंतवणूकदार संरक्षण कवच",
        "sub": "थांबा. विचार करा. फसवणूक टाळा. भांडवल वाचवा.",
        "tab1": "निर्णय नोंदवही",
        "tab2": "फसवणूक तपासक",
        "tab3": "घसरण सिम्युलेटर",
        "cb_warning": "⚠️ सर्किट ब्रेकर सक्रिय ⚠️",
        "cb_text": "घाईघाईत घेतलेले निर्णय टाळण्यासाठी सिस्टीम 1 तास लॉक आहे.",
        "q_asset": "शेअर किंवा मालमत्तेचे नाव",
        "q_amount": "गुंतवणूक रक्कम (₹)",
        "q_reason": "तुम्ही हा निर्णय का घेत आहात?:",
        "q_horizon": "कालावधी",
        "btn_journal": "नोंद करा",
        "journal_success": "✅ निर्णय यशस्वीरीत्या नोंदवला गेला आहे.",
        "scam_alert": "🚨 फसवणुकीचा इशारा 🚨",
        "scam_msg": "तुमच्या उत्तरात संशयास्पद शब्द आहेत. सेबी नोंदणीकृत सल्लागार हमी परतावा देत नाहीत.",
        "history_title": "मागील निर्णय",
        "history_empty": "अद्याप कोणताही निर्णय नोंदवलेला नाही.",
        "scanner_title": "टिप स्कॅनर",
        "scanner_desc": "व्हॉट्सॲप किंवा टेलिग्राम संदेशांची सत्यता तपासा.",
        "scanner_input": "संदेश येथे पेस्ट करा:",
        "scanner_btn": "तपासा",
        "scanner_clean": "✅ कोणताही संशयास्पद शब्द आढळला नाही.",
        "scanner_risk": "⚠️ उच्च जोखीम इशारा ⚠️ हा फसवणुकीचा प्रयत्न असू शकतो.",
        "sim_title": "बाजार घसरण सिम्युलेटर",
        "sim_desc": "गुंतवणूक करण्यापूर्वी बाजार घसरल्यास काय होईल ते पहा.",
        "sim_input": "रक्कम टाका (₹):",
        "sim_calc": "परिणाम तपासा"
    },
    "বাংলা (Bengali)": {
        "title": "🛡️ নির্ণয়: বিনিয়োগকারী সুরক্ষা কবচ",
        "sub": "থামুন। ভাবুন। প্রতারণা এড়ান। মূলধন বাঁচান।",
        "tab1": "সিদ্ধান্তের ডায়েরি",
        "tab2": "প্রতারণা পরীক্ষক",
        "tab3": "পতন সিমুলেটর",
        "cb_warning": "⚠️ সার্কিট ব্রেকার সক্রিয় ⚠️",
        "cb_text": "তাড়াহুড়ো করে সিদ্ধান্ত নেওয়া আটকাতে সিস্টেম ১ ঘণ্টার জন্য লক করা হয়েছে।",
        "q_asset": "শেয়ার বা সম্পদের নাম",
        "q_amount": "বিনিয়োগের পরিমাণ (₹)",
        "q_reason": "কেন এই সিদ্ধান্ত নিচ্ছেন? (ব্যাখ্যা করুন):",
        "q_horizon": "সময়কাল",
        "btn_journal": "সিদ্ধান্ত নথিভুক্ত করুন",
        "journal_success": "✅ সিদ্ধান্ত সফলভাবে সংরক্ষিত হয়েছে।",
        "scam_alert": "🚨 প্রতারণার সতর্কতা 🚨",
        "scam_msg": "আপনার ব্যাখ্যায় ঝুঁকিপূর্ণ শব্দ রয়েছে। সেবি নিবন্ধিত উপদেষ্টারা নিশ্চিত রিটার্ন প্রতিশ্রুতি দেন না।",
        "history_title": "পূর্ববর্তী সিদ্ধান্ত",
        "history_empty": "এখনও কোনও সিদ্ধান্ত নথিভুক্ত করা হয়নি।",
        "scanner_title": "টিপ স্ক্যানার",
        "scanner_desc": "সন্দেহজনক মেসেজ বা সামাজিক মাধ্যমের টিপ যাচাই করুন।",
        "scanner_input": "মেসেজটি এখানে পেস্ট করুন:",
        "scanner_btn": "বিশ্লেষণ করুন",
        "scanner_clean": "✅ কোনও প্রতারণামূলক শব্দ মেলেনি।",
        "scanner_risk": "⚠️ উচ্চ ঝুঁকি সতর্কতা ⚠️ এই মেসেজটি প্রতারণামূলক হতে পারে।",
        "sim_title": "বাজার পতন সিমুলেটর",
        "sim_desc": "টাকা লাগানোর আগে বাজার পতনের ঝুঁকি অনুভব করুন।",
        "sim_input": "বিনিয়োগের পরিমাণ লিখুন (₹):",
        "sim_calc": "প্রভাব দেখুন"
    }
}

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
        if time.time() - last_trade_time < 3600:
            return True
    return False

def scan_for_red_flags(text):
    text_lower = text.lower()
    return [word for word in RED_FLAGS if word in text_lower]

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="Nirnaya - Investor Shield", page_icon="🛡", layout="centered")

# Language Selector
selected_lang = st.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ / भाषा चुनें", 
    list(TRANSLATIONS.keys())
)
ui = TRANSLATIONS[selected_lang]

st.title(ui["title"])
st.caption(ui["sub"])

tab1, tab2, tab3 = st.tabs([ui["tab1"], ui["tab2"], ui["tab3"]])

# TAB 1: DECISION JOURNAL
with tab1:
    journal_data = load_journal()
    
    if check_circuit_breaker(journal_data):
        st.error(ui["cb_warning"])
        st.write(ui["cb_text"])
    else:
        with st.form("decision_form"):
            asset = st.text_input(ui["q_asset"], placeholder="e.g. Tata Motors / Nifty ETF")
            amount = st.number_input(ui["q_amount"], min_value=100, step=500, value=5000)
            reason = st.text_area(ui["q_reason"], placeholder="e.g. Long-term corporate performance, not social tips...")
            horizon = st.selectbox(ui["q_horizon"], ["Short-term / അಲ್ಪಾವಧಿ", "Long-term / ದೀರ್ಘಾವಧಿ"])
            
            submitted = st.form_submit_button(ui["btn_journal"])
            
            if submitted:
                if asset.strip() and reason.strip():
                    flags = scan_for_red_flags(reason)
                    if flags:
                        st.error(ui["scam_alert"])
                        st.warning(f"{ui['scam_msg']}\n\n**Flagged markers:** `{', '.join(flags)}`")
                    else:
                        entry = {
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
                    st.warning("Please fill out all required fields.")

    st.divider()
    st.subheader(ui["history_title"])
    if journal_data:
        for item in reversed(journal_data[-5:]):
            with st.expander(f"📌 {item.get('asset', 'Unknown')} - ₹{item.get('amount', 0)} ({item.get('time_str', 'Logged')})"):
                st.write(f"**Horizon:** {item.get('horizon')}")
                st.write(f"**Reasoning:** {item.get('reason')}")
    else:
        st.info(ui["history_empty"])

# TAB 2: WHATSAPP / TELEGRAM TIP SCANNER
with tab2:
    st.subheader(ui["scanner_title"])
    st.write(ui["scanner_desc"])
    
    msg_input = st.text_area(ui["scanner_input"], height=120, placeholder="Paste forwarded advice or message...")
    
    if st.button(ui["scanner_btn"]):
        if msg_input.strip():
            found = scan_for_red_flags(msg_input)
            if found:
                st.error(ui["scanner_risk"])
                st.markdown(f"> **Detected Deceptive Buzzwords:** `{', '.join(found)}`")
                st.info("💡 **SEBI Advisory Rule:** Genuine registered advisors are legally prohibited from guaranteeing profits or sharing trading tips on unofficial channels.")
            else:
                st.success(ui["scanner_clean"])
        else:
            st.warning("Please paste a message first.")

# TAB 3: DOWNSIDE STRESS SIMULATOR (TRACK C)
with tab3:
    st.subheader(ui["sim_title"])
    st.write(ui["sim_desc"])
    
    sim_capital = st.number_input(ui["sim_input"], min_value=1000, step=1000, value=10000)
    
    if st.button(ui["sim_calc"]):
        st.write("### What a normal market correction looks like:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            loss_10 = sim_capital * 0.10
            st.metric(label="Mild Pullback (-10%)", value=f"₹{sim_capital - loss_10:,.0f}", delta=f"-₹{loss_10:,.0f}")
            st.caption("Common multiple times a year.")
            
        with c2:
            loss_25 = sim_capital * 0.25
            st.metric(label="Correction (-25%)", value=f"₹{sim_capital - loss_25:,.0f}", delta=f"-₹{loss_25:,.0f}")
            st.caption("Occurs during bear phases.")
            
        with c3:
            loss_50 = sim_capital * 0.50
            st.metric(label="Major Crash (-50%)", value=f"₹{sim_capital - loss_50:,.0f}", delta=f"-₹{loss_50:,.0f}")
            st.caption("Historic panics (e.g. 2008, 2020).")
            
        st.warning("⚠️ **Resilience Self-Check:** If seeing a -₹{:,.0f} drop would force you to borrow money or skip basic household expenses, do not invest this capital into equity instruments.".format(loss_25))
