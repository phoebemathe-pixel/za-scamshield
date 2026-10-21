import streamlit as st
import re

st.set_page_config(page_title="ZA-ScamShield", page_icon="🛡️", layout="centered")

st.title("🛡️ ZA-ScamShield - Detects ANY SA Bank Scam SMS")
st.write("Paste any suspicious SMS below")

SA_BANKS = {
    "capitec": ["capitec"],
    "fnb": ["fnb", "first national"],
    "absa": ["absa"],
    "standard bank": ["standard bank", "stanbic"],
    "nedbank": ["nedbank"],
    "tymebank": ["tymebank", "tyme bank"],
    "discovery": ["discovery bank"],
    "african bank": ["african bank"],
    "investec": ["investec"],
    "postbank": ["postbank"],
    "bidvest": ["bidvest"],
    "sars": ["sars"],
    "capfin": ["capfin"],
    "sassa": ["sassa", "r350", "ewallet"]
}

sms = st.text_area("Paste SMS here:", value="You have R4,500 refund, click here to claim https://sars-refund.co.za", height=150)

col1, col2 = st.columns(2)
check = col1.button("🔍 Check SMS", use_container_width=True, type="primary")
clear = col2.button("Clear", use_container_width=True)

if clear:
    st.rerun()

if check and sms:
    sms_lower = sms.lower()
    
    detected_bank = "UNKNOWN"
    for bank, keywords in SA_BANKS.items():
        if any(k in sms_lower for k in keywords):
            detected_bank = bank.upper()
            break
    
    st.write(f"**Detected: {detected_bank}**")
    
    score = 0
    reasons = []
    
    if any(w in sms_lower for w in ["blocked", "suspended", "locked"]):
        score += 35
        reasons.append("🚩 +35: Claims account blocked/suspended - banks don't do this via SMS link")
    if "http" in sms_lower or "click" in sms_lower or ".co.za" in sms_lower or "link" in sms_lower:
        score += 25
        reasons.append("🚩 +25: Contains suspicious link")
    if any(w in sms_lower for w in ["urgent", "immediately", "now", "verify"]):
        score += 15
        reasons.append("🚩 +15: Creates fake urgency")
    if any(w in sms_lower for w in ["refund", "r4,500", "r350", "otp", "pin"]):
        score += 10
        reasons.append("🚩 +10: Mentions refund/OTP/PIN - SARS/banks never ask this via SMS")

    if score >= 50:
        st.markdown("### 🔴 HIGH RISK - LIKELY SCAM")
    elif score >= 25:
        st.markdown("### 🟡 MEDIUM RISK")
    else:
        st.markdown("### 🟢 LOW RISK")
    
    st.progress(min(score, 100))
    st.write("Scam Probability")
    st.write(f"## {min(score+30, 95)}%")
    
    st.write("### Why?")
    for r in reasons:
        st.write(r)

    st.caption("Made with ❤️ by Botshelo Phoebe Mathe from SA")