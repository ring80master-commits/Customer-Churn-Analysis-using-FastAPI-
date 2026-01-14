from fastapi import FastAPI
import pickle
import pandas as pd
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# 1. मॉडल लोड करना
MODEL_PATH = "model/random_forest_model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# 2. Pydantic Model (Input format)
class ChurnInput(BaseModel):
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: float
    PhoneService: int
    MultipleLines: int
    OnlineSecurity: int
    OnlineBackup: int
    DeviceProtection: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    PaperlessBilling: int
    MonthlyCharges: float
    TotalCharges: float
    # कैटेगरीज के लिए हम स्ट्रिंग या इंट ले सकते हैं, 
    # पर यहाँ हम वही वैल्यू लेंगे जो आपने टेस्ट में डाली थी
    InternetService: int # 0: DSL, 1: Fiber, 2: No
    Contract: int        # 0: Month-to-month, 1: One year, 2: Two year
    PaymentMethod: int   # 0: Electronic check, 1: Mailed, 2: Bank transfer, 3: Credit card

def scale_val(val, min_v, max_v):
    return (val - min_v) / (max_v - min_v)

@app.post("/predict")
def predict_churn(data: ChurnInput):
    # डेटा को डिक्शनरी में बदलें
    d = data.dict()
    
    # एक्स्ट्रा प्रोसेसिंग: One-Hot Encoding को मैन्युअल रूप से सेट करना
    # मॉडल इन कॉलम्स की उम्मीद कर रहा है (drop_first=True के बाद)
    
    # InternetService logic
    d['InternetService_Fiber optic'] = 1 if d['InternetService'] == 1 else 0
    d['InternetService_No'] = 1 if d['InternetService'] == 2 else 0
    
    # Contract logic
    d['Contract_One year'] = 1 if d['Contract'] == 1 else 0
    d['Contract_Two year'] = 1 if d['Contract'] == 2 else 0
    
    # PaymentMethod logic (Assuming Bank Transfer was dropped)
    d['PaymentMethod_Credit card (automatic)'] = 1 if d['PaymentMethod'] == 3 else 0
    d['PaymentMethod_Electronic check'] = 1 if d['PaymentMethod'] == 0 else 0
    d['PaymentMethod_Mailed check'] = 1 if d['PaymentMethod'] == 1 else 0

    # न्यूमेरिकल स्केलिंग
    d['tenure'] = scale_val(d['tenure'], 0, 72)
    d['MonthlyCharges'] = scale_val(d['MonthlyCharges'], 18.25, 118.75)
    d['TotalCharges'] = scale_val(d['TotalCharges'], 0, 8684.8)

    # उन ओरिजिनल कॉलम्स को हटा दें जो अब OHE में बदल चुके हैं
    for col in ['InternetService', 'Contract', 'PaymentMethod']:
        d.pop(col)

    # 3. कॉलम्स का क्रम (Order) वही होना चाहिए जो ट्रेनिंग के समय था
    # यहाँ उन सभी कॉलम्स की लिस्ट है जो मॉडल को चाहिए
    feature_order = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
        'InternetService_Fiber optic', 'InternetService_No',
        'Contract_One year', 'Contract_Two year',
        'PaymentMethod_Credit card (automatic)',
        'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check'
    ]
    
    # DataFrame को सही आर्डर में बनाना
    df = pd.DataFrame([d])[feature_order]
    
    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    
    return {
        "churn": "Yes" if int(prediction) == 1 else "No",
        "probability": f"{round(float(prob) * 100, 2)}%"
    }
