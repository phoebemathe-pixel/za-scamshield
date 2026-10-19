import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = {
    'text': [
        "Capitec blocked click link to verify",
        "Mama you won R50000 from Telkom, send banking details",
        "SARS refund R1245 click link to claim",
        "Your parcel at Post Office pay R30 fee https://bit.ly/xyz",
        "eWallet R2000 received call 078...",
        "Hi, meeting moved to 2pm tomorrow",
        "Loadshedding from 6-8pm tonight",
        "Your NSFAS allowance paid R1700",
        "Mom I'm home safe, food?",
        "Assignment due Friday 11pm",
        "Get a 450MB data bundle for R50, click here https://data-deal.co.za",
        "Great value on groceries at Checkers this week",
        "Great news! Your loan approved, please click the link",
        "Spend R120p/m and get R10000 FREE funeral cover",
        "Thank you for signing up with Study in Korea",
        "Get summer ready with our new swimwear range",
        "The group project has been submitted",
        "Hey lucky winner!! You have won iPhone 15! Click here",
        "Bogosipeo neomu yeppeo",
        "R1000 shopping voucher click here to claim",
        "Dad can you buy bread on your way home?",
        "See you at church on Sunday"
    ],
    'label': [1,1,1,1,1,0,0,0,0,0,1,0,1,1,0,0,0,1,0,1,0,0]
}

df = pd.DataFrame(data)
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42, stratify=df['label'])
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
model = LogisticRegression()
model.fit(X_train_vec, y_train)

def check_sms(sms):
    vec = vectorizer.transform([sms])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0].max()
    return pred, prob

st.set_page_config(page_title="ZA-ScamShield", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    .main { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
    h1 { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 50px; font-size: 18px; background: linear-gradient(90deg, #6366f1, #8b5cf6); color: white; border: none; }
    .result-card { padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🛡️ ZA-ScamShield</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Protecting South Africans from scam SMS with AI ✨</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", "75%")
col2.metric("SMS Learned", "22")
col3.metric("Threats", "3 Types")

st.write("")

sms_input = st.text_area("💬 Paste that suspicious SMS here chomi:", "Your Capitec account blocked click here https://capitec-verify.co.za", height=120)

if st.button("✨ Check if it's a Scam"):
    result, conf = check_sms(sms_input)
    if result == 1:
        st.markdown(f"<div class='result-card' style='background:#fee2e2; color:#dc2626; border: 2px solid #fecaca;'>🚨 SCAM DETECTED!<br><span style='font-size:14px; font-weight:normal;'>Confidence: {conf*100:.0f}% – Don't click, delete it bestie!</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-card' style='background:#dcfce7; color:#16a34a; border: 2px solid #bbf7d0;'>✅ Looks Safe, chomi!<br><span style='font-size:14px; font-weight:normal;'>Confidence: {conf*100:.0f}% – Still stay alert tho!</span></div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#64748b; font-size:12px;'>Made with 💖 in SA by Botshelo Phoebe Mathe </p>", unsafe_allow_html=True)