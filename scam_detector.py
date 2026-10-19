import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

data = {
    'text': [
        "Your Capitec account blocked, click https://capitec-verify.co.za",
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
        "Great value on groceries at Checkers this week, check the app for deals",
        "Great news! Your application for the loan has been approved, please click the link to proceed",
        "Spend R120p/m and get R10000 FREE funeral cover, click here to sign up",
        "Thank you for signing up with Study In Korea, please check your email for further instructions",
        "Get summer ready with our new range of swimwear. Get R150 OFF R450 by clicking this link https://swimwear-deals.co.za",
        "The group project has been submitted, please check the shared drive for the files",
        "Hey lucky winner!! You have won a brand new iPhone 15! Click here to claim your prize: https://iphone-giveaway.co.za",
        "Bogosipeo...",
        "Claim your free R1000 shopping voucher now! Click here to claim: https://shopping-voucher.co.za",
        
 ],
    'label': [1,1,1,1,1,0,0,0,0,0,1,0,1,1,0,0,0,1,0,1]
}

df = pd.DataFrame(data)
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42, stratify=df['label'])
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
model = LogisticRegression()
model.fit(X_train_vec, y_train)

acc = accuracy_score(y_test, model.predict(vectorizer.transform(X_test)))
print(f"Accuracy: {acc*100:.1f}% ")

def check_sms(sms):
    vec = vectorizer.transform([sms])
    pred = model.predict(vec)[0]
    return "SCAM DETECTED - Don't click!" if pred==1 else "Looks Safe"

print(check_sms("Your Capitec account is locked, verify here https://fake-link.co.za"))
print(check_sms("Hi chomi are you home?"))