import streamlit as st
import re

st.set_page_config(page_title="ZA-ScamShield", page_icon="🛡️", layout="centered")

st.title("🛡️ ZA-ScamShield - Detects ANY SA Bank Scam SMS")
st.write("Paste any Capitec / FNB / ABSA / Standard Bank / Nedbank / TymeBank / SARS scam SMS")

# --- SA BANKS + SARS ---
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
    "capfin": ["capfin"]
}

def is_scam(sms):
    sms_lower = sms.lower()
    keywords = ["urgent", "verify", "blocked", "suspended", "click", "link", "http", "otp", "pin", "sars refund", "ewallet", "r350", "sassa"]
    bank_found = any(any(k in sms_lower for k in v) for v in SA_BANKS.values())
    scam_word = any(k in sms_lower for k in keywords)
    return bank_found and scam_word

sms = st.text_area("Paste SMS here:")

if st.button("Check SMS"):
    if is_scam(sms):
        st.error("🚨 SCAM DETECTED! Don't click any link!")
    else:
        st.success("✅ Looks safe")