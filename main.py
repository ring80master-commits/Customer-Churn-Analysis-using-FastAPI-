from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Static और Templates फोल्डर को कॉन्फ़िगर करना
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# मॉडल लोड करना
MODEL_PATH = "model/random_forest_model.pkl"
model = pickle.load(open(MODEL_PATH, "rb"))

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
    InternetService: int
    Contract: int
    PaymentMethod: int

def scale_val(val, min_v, max_v):
    return (val - min_v) / (max_v - min_v)

# होमपेज रूट - यहाँ से index.html लोड होगी
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict_churn(data: ChurnInput):
    d = data.dict()
    
    # OHE Logic (जैसा हमने पिछली बार किया था)
    d['InternetService_Fiber optic'] = 1 if d['InternetService'] == 1 else 0
    d['InternetService_No'] = 1 if d['InternetService'] == 2 else 0
    d['Contract_One year'] = 1 if d['Contract'] == 1 else 0
    d['Contract_Two year'] = 1 if d['Contract'] == 2 else 0
    d['PaymentMethod_Credit card (automatic)'] = 1 if d['PaymentMethod'] == 3 else 0
    d['PaymentMethod_Electronic check'] = 1 if d['PaymentMethod'] == 0 else 0
    d['PaymentMethod_Mailed check'] = 1 if d['PaymentMethod'] == 1 else 0

    # Scaling
    d['tenure'] = scale_val(d['tenure'], 0, 72)
    d['MonthlyCharges'] = scale_val(d['MonthlyCharges'], 18.25, 118.75)
    d['TotalCharges'] = scale_val(d['TotalCharges'], 0, 8684.8)

    for col in ['InternetService', 'Contract', 'PaymentMethod']:
        d.pop(col)

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
    
    df = pd.DataFrame([d])[feature_order]
    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    
    return {
        "churn": "Yes" if int(prediction) == 1 else "No",
        "probability": f"{round(float(prob) * 100, 2)}%"
    }
    