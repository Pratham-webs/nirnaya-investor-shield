import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

# --- GEN Z CUSTOM CSS (NEON & ROUNDED) ---
st.set_page_config(page_title="Nirnaya - Investor Shield", page_icon="🛡", layout="centered")
st.markdown("""
    <style>
    /* Gradient text for titles */
    .genz-title {
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
    }
    /* Sleek buttons */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background: linear-gradient(90deg, #4ECDC4 0%, #556270 100%);
        color: white;
        border: none;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    /* Rounded input boxes */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 15px !important;
        border: 1px solid #4ECDC4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND LOGIC ---
RED_FLAGS = ["guaranteed", "sure shot", "telegram", "whatsapp", "multibagger", "100%", "ಖಚಿತ", "ಗ್ಯಾರಂಟಿ"]

def load_journal():
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

def save_journal(data):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(data, file, indent=4)

def check_circuit_breaker(journal_data, username):
    # Filter trades by this specific user
    user_trades = [t for t in journal_data if t.get("user") == username]
    if len(user_trades) >= 3:
        last_trade_time = user_trades[-1].get("timestamp", 0)
        if time.time() - last_trade_time < 3600:
            return True
    return False

def scan_for_red_flags(text):
    text_lower = text.lower()
    return [word for word in RED_FLAGS if word in text_lower]

# --- SESSION AUTHENTICATION (LOGIN PAGE) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown('<h1 class="genz-title">🛡️ NIRNAYA</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Enter the zone. Protect your capital.</p>", unsafe_allow_html=True)
    
    st.write("")
    with st.form("login_form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            avatar = st.selectbox("Avatar", ["🧑‍💻", "🚀", "💎", "🦍", "📈"])
        with col2:
            username = st.text_input("Choose your Nickname", placeholder="e.g. DiamondHands99")
        
        login_btn = st.form_submit_button("Enter Dashboard")
        
        if login_btn:
            if username.strip():
                st.session_state['logged_in'] = True
                st.session_state['username'] = username.strip()
                st.session_state['avatar'] = avatar
                st.rerun()
            else:
                st.error("Bruh, you need a nickname to enter.")

# --- MAIN DASHBOARD (FRONTEND) ---
else:
    st.markdown(f"### {st.session_state['avatar']} Welcome back, **{st.session_state['username']}**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Journal", "🕵️‍♂️ Scam Checker", "💥 Simulator", "📊 My Vibe Check"])
    
    journal_data = load_journal()
    
    # TAB 1: DECISION JOURNAL
    with tab1:
        if check_circuit_breaker(journal_data, st.session_state['username']):
            st.error("⚠️ COOL DOWN ACTIVATED ⚠️")
            st.write("You are moving too fast. Market isn't running away. Locked for 1 hour.")
        else:
            with st.form("decision_form"):
                asset = st.text_input("Asset Name", placeholder="e.g. Tata Motors")
                amount = st.number_input("Amount (₹)", min_value=100, step=500, value=5000)
                reason = st.text_area("Your Thesis", placeholder="Why this? Why now?")
                horizon = st.selectbox("Horizon", ["Short-term (Days/Weeks)", "Long-term (Years)"])
                
                if st.form_submit_button("Log Decision"):
                    if asset and reason:
                        flags = scan_for_red_flags(reason)
                        if flags:
                            st.error("🚨 RED FLAG DETECTED 🚨")
                            st.warning(f"Your reasoning sounds like a scam tip: `{', '.join(flags)}`")
                        else:
                            entry = {
                                "user": st.session_state['username'],
                                "asset": asset,
                                "amount": amount,
                                "reason": reason,
                                "horizon": horizon,
                                "timestamp": time.time(),
                                "time_str": time.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            journal_data.append(entry)
                            save_journal(journal_data)
                            st.success("✅ Trade logged securely.")
                    else:
                        st.warning("Fill all fields.")

    # TAB 2 & 3: SCANNER & SIMULATOR
    with tab2:
        st.write("### The WhatsApp Tip Scanner")
        msg = st.text_area("Paste suspicious message here:")
        if st.button("Analyze Vibe"):
            if msg:
                found = scan_for_red_flags(msg)
                if found:
                    st.error("⚠️ HUGE RED FLAG. This is a classic pump-and-dump.")
                else:
                    st.success("✅ Looks clean, but always verify SEBI registration.")
    
    with tab3:
        st.write("### Market Crash Simulator")
        sim_cap = st.number_input("Capital to test (₹)", value=10000)
        if st.button("Stress Test"):
            c1, c2, c3 = st.columns(3)
            c1.metric("10% Drop", f"₹{sim_cap * 0.9:,.0f}", f"-₹{sim_cap * 0.1:,.0f}")
            c2.metric("25% Drop", f"₹{sim_cap * 0.75:,.0f}", f"-₹{sim_cap * 0.25:,.0f}")
            c3.metric("50% Crash", f"₹{sim_cap * 0.5:,.0f}", f"-₹{sim_cap * 0.5:,.0f}")

    # TAB 4: USER ANALYTICS (NEW FEATURE)
    with tab4:
        st.write("### 🧠 Your Behavioral Analytics")
        user_history = [t for t in journal_data if t.get("user") == st.session_state['username']]
        
        if not user_history:
            st.info("Log some trades in the Journal first so I can analyze your vibe.")
        else:
            total_trades = len(user_history)
            short_term = sum(1 for t in user_history if "Short-term" in t.get("horizon", ""))
            total_amount = sum(t.get("amount", 0) for t in user_history)
            
            # Stat Cards
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Decisions", total_trades)
            col2.metric("Total Capital Tracked", f"₹{total_amount:,.0f}")
            col3.metric("Short-Term Focus", f"{int((short_term/total_trades)*100)}%")
            
            st.divider()
            st.write("#### 🔮 System Verdict:")
            
            # Algorithmic Persona Generation
            if short_term > (total_trades / 2) and total_trades >= 3:
                st.error("**Persona: The FOMO Chaser 📉**")
                st.write("You are logging a lot of short-term trades rapidly. You might be chasing momentum rather than investing. Slow down.")
            elif total_trades >= 3:
                st.success("**Persona: The Zen Master 🧘‍♂️**")
                st.write("You are heavily focused on the long-term. You ignore the noise and build wealth patiently. Major W.")
            else:
                st.info("Keep logging decisions to unlock your investor persona profile!")
        
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
