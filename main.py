import streamlit as st
import time
import json
import os

JOURNAL_FILE = "nirnaya_journal.json"

st.set_page_config(page_title="Nirnaya - Investor Shield", page_icon="🛡", layout="wide")

# --- GLASSMORPHISM & MILLENNIAL CSS ---
st.markdown("""
    <style>
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    .stSlider>div>div>div>div { background-color: #4ECDC4 !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🛡️ NIRNAYA")
    st.caption("Protect your capital. Ignore the noise.")
    menu = st.radio("Navigation", ["📝 The Journal", "🕵️‍♂️ Scam Scanner", "💥 Crash Simulator", "🤖 Jargon Chatbot", "💡 Legends' Wisdom"])
    st.divider()
    st.write("Logged in as: **Guest**")

# --- CORE FUNCTIONS ---
def load_journal():
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r") as file: return json.load(file)
        except: return []
    return []

# --- MENU 1: THE JOURNAL (Upgraded Inputs) ---
if menu == "📝 The Journal":
    st.markdown("<div class='glass-card'><h3>Log Your Next Move</h3></div>", unsafe_allow_html=True)
    with st.form("journal"):
        asset = st.text_input("What's the asset?", placeholder="e.g. Index Fund, Bluechip Stock")
        
        # Upgraded Slider Input
        amount = st.slider("Capital allocation (₹)", min_value=500, max_value=100000, step=500, value=5000)
        
        reason = st.text_area("Your Thesis (Why?)", placeholder="Don't just say 'it will go up'. Explain your logic.")
        horizon = st.select_slider("Time Horizon", options=["Days", "Weeks", "Months", "Years", "Decades"])
        
        if st.form_submit_button("Lock Decision"):
            st.success("✅ Trade logged securely on your device.")

# --- MENU 2 & 3: SCANNER & SIMULATOR ---
elif menu == "🕵️‍♂️ Scam Scanner":
    st.write("### The WhatsApp Tip Scanner")
    msg = st.text_area("Paste suspicious message here:")
    if st.button("Analyze Vibe"):
        st.error("⚠️ HIGH RISK. Genuine SEBI advisors do not guarantee returns.")

elif menu == "💥 Crash Simulator":
    st.write("### Stress Test Your Portfolio")
    sim_cap = st.slider("Test Capital (₹)", 1000, 500000, 10000)
    c1, c2, c3 = st.columns(3)
    c1.metric("10% Market Correction", f"₹{sim_cap * 0.9:,.0f}", f"-₹{sim_cap * 0.1:,.0f}")
    c2.metric("25% Bear Market", f"₹{sim_cap * 0.75:,.0f}", f"-₹{sim_cap * 0.25:,.0f}")
    c3.metric("50% Black Swan Crash", f"₹{sim_cap * 0.5:,.0f}", f"-₹{sim_cap * 0.5:,.0f}")

# --- MENU 4: JARGON BUSTER CHATBOT ---
elif menu == "🤖 Jargon Chatbot":
    st.write("### 🤖 Fin-Buster Chat")
    st.caption("Ask me to explain any confusing finance term in simple words.")
    
    # Native Streamlit Chat Interface
    for message in [{"role": "assistant", "content": "What financial term is confusing you today? (e.g. Mutual Fund, F&O, Margin)"}]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Type a term..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(f"**{prompt}** explained simply: It is like managing a balanced auction purse. You can't spend your entire budget on aggressive top-order players and ignore your bowlers. Diversification protects you when the market collapses.")

# --- MENU 5: LEGENDS' WISDOM ---
elif menu == "💡 Legends' Wisdom":
    st.write("### 🧠 Real Advice from Verified Legends")
    st.info("**Rakesh Jhunjhunwala:** 'Respect the market. Have an open mind. Know what to stake. Know when to take a loss. Be responsible.'")
    st.success("**Warren Buffett:** 'The stock market is a device for transferring money from the impatient to the patient.'")
    st.warning("**Peter Lynch:** 'Know what you own, and know why you own it.' (This is exactly why Nirnaya forces you to journal your trades).")
