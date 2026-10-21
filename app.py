import streamlit as st
import re

st.set_page_config(page_title="ZA-ScamShield", page_icon="🛡️", layout="centered")

st.title("🛡️ ZA-ScamShield - Detects ANY SA Bank Scam SMS")
st.write("Paste any Capitec / FNB / ABSA / Standard Bank / Nedbank / TymeBank SMS and check if it's a scam. 100% offline.")

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

SCAM_PATTERNS = [
    (r"account.*(blocked|suspended|frozen|locked|compromised)", "Claims account blocked/suspended - banks don't do this via SMS link", 35),
    (r"(verify|validate|update).*(account|details|kyc|information)", "Asks you to verify/update via link", 30),
    (r"https?://|bit\.ly|tinyurl|t\.me|wa\.me", "Contains suspicious link", 25),
    (r"\b(otp|pin|password|cvv)\b", "Asks for OTP/PIN/Password - REAL banks NEVER ask this on SMS", 40),
    (r"urgent|immediately|within 24|24 hours|act now", "Creates fake urgency", 15),
    (r"sars.*refund|refund.*sars|tax refund", "Fake SARS refund scam - very common in SA", 30),
    (r"click.*(here|link|below)", "Tells you to click a link", 20),
    (r"dear (customer|client|valued)", "Generic greeting, not your name", 10),
    (r"\d{3}-\d{4}|won.*prize|lottery", "Lottery/prize scam", 25),
]

SAFE_PATTERNS = [
    (r"you spent|purchase of R|withdrawal of R|balance is R|paid R", "Looks like a real transaction notification", -30),
    (r"reference: |ref no|statement available on app", "Mentions app, not link", -20),
]

def analyze_sms(sms_text):
    sms_lower = sms_text.lower()
    score = 10  # base
    reasons = []
    
    detected_bank = "Unknown"
    for bank, keywords in SA_BANKS.items():
        for kw in keywords:
            if kw in sms_lower:
                detected_bank = bank.upper()
                break

    for pattern, reason, points in SCAM_PATTERNS:
        if re.search(pattern, sms_lower):
            score += points
            reasons.append(f"🚩 +{points}: {reason}")

    for pattern, reason, points in SAFE_PATTERNS:
        if re.search(pattern, sms_lower):
            score += points  # points is negative
            reasons.append(f"✅ {points}: {reason}")

    # Cap score 0-100
    score = max(0, min(100, score))
    
    if score >= 75:
        verdict = "🔴 HIGH RISK - LIKELY SCAM"
        color = "red"
    elif score >= 45:
        verdict = "🟡 SUSPICIOUS - Be Careful"
        color = "orange"
    else:
        verdict = "🟢 LIKELY SAFE - But stay alert"
        color = "green"
        
    return score, verdict, color, detected_bank, reasons

# --- UI ---
sms = st.text_area("Paste the SMS here:", height=150, placeholder="e.g. Capitec: Your account has been blocked, click https://capitec-secure.co.za to verify immediately")

col1, col2 = st.columns([1,1])
with col1:
    check_btn = st.button("🔍 Check SMS", type="primary", use_container_width=True)
with col2:
    st.button("Clear", on_click=lambda: st.session_state.clear(), use_container_width=True)

if check_btn:
    if not sms or len(sms) < 10:
        st.error("Paste a full SMS first chomi!")
    else:
        score, verdict, color, bank, reasons = analyze_sms(sms)
        
        st.markdown(f"### Detected: {bank}")
        st.markdown(f"### {verdict}")
        st.progress(score / 100)
        st.metric("Scam Probability", f"{score}%")
        
        st.subheader("Why?")
        for r in reasons:
            st.write(r)
        
        st.divider()
        if score >= 45:
            st.warning("**What to do:**\n1. DON'T click any link\n2. DON'T share OTP/PIN\n3. Open your bank app YOURSELF to check\n4. Call your bank's official number on back of card")
        else:
            st.success("This looks like a normal bank notification, but always open your banking APP directly, never via SMS link.")

st.divider()
st.caption("Built for SA by a SA student 🇿🇦 | Detects Capitec, FNB, ABSA, Standard Bank, Nedbank, TymeBank, Discovery, African Bank, Investec, Postbank + SARS scams | 100% offline - works during loadshedding")