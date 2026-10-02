# 🛡️ Nirnaya: Investor Resilience Shield

**A national, public-good hackathon submission for the SEBI & NSDL SANGYAN Investor Resilience Hackathon.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nirnaya-investor-shield.streamlit.app)
*(Click to view Live Demo)*

## 🎯 The Challenge
India's retail investor base is booming, especially in non-metro and Tier-2/3 cities. However, market access has outpaced financial confidence. First-time investors frequently fall victim to impulsive FOMO trading, social media "tips," and fraudulent schemes. 

## 💡 The Solution: Nirnaya
Nirnaya is a behavioral resilience terminal and public-good infrastructure designed to help users pause, reflect, and avoid scams. It integrates multiple hackathon tracks into a single, seamless, regional-language-first application.

### Targeted Hackathon Tracks:
*   **Track D: Financial Habits & Behavioural Resilience:** Features a "Decision Journal" with a mandatory cooling-off circuit breaker that locks out impulsive, rapid-fire revenge trading.
*   **Track A & E: Digital Fraud & Misinformation:** Includes a heuristic message scanner that evaluates forwarded WhatsApp/Telegram tips for deceptive pump-and-dump keywords.
*   **Track C: Investor Education for Bharat:** Features an interactive Downside Stress Simulator and a plain-language "Fin-Buster" AI chatbot to deconstruct complex jargon.

## 🚀 Key Features
*   **Bharat-First Usability:** Full UI support for 7 regional languages (English, Hindi, Kannada, Telugu, Tamil, Marathi, Bengali) catering directly to Tier-2/3 investors.
*   **Privacy by Design:** Zero cloud harvesting. User decisions are logged entirely to a local `JSON` state, completely isolating personally identifiable financial data.
*   **Zero Commercial Funnels:** Strictly adheres to guardrails—no stock tips, no broker links, and no price predictions. 

## 🛠️ Technology Stack
*   **Frontend & Routing:** Python (Streamlit) featuring custom Glassmorphism CSS and responsive widget architecture.
*   **Backend & Data State:** Python runtime with local `JSON` dictionary appending for secure session history.
*   **Deployment:** Streamlit Community Cloud.

## 💻 Local Setup Instructions
To run this project locally on your machine:

1. Clone the repository:
   ```bash
   git clone [https://github.com/pratham-webs/nirnaya-investor-shield.git](https://github.com/pratham-webs/nirnaya-investor-shield.git)
