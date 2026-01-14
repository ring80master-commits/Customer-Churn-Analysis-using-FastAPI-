async function predict() {
    const getVal = (id) => parseInt(document.getElementById(id).value);
    const getFloat = (id) => parseFloat(document.getElementById(id).value);

    const inputData = {
        gender: getVal('gender'),
        SeniorCitizen: getVal('seniorCitizen'),
        Partner: getVal('partner'),
        Dependents: getVal('dependents'),
        tenure: getFloat('tenure'),
        PhoneService: 1, // Default
        MultipleLines: 0, // Default
        OnlineSecurity: getVal('onlineSecurity'),
        OnlineBackup: 0,
        DeviceProtection: 0,
        TechSupport: getVal('techSupport'),
        StreamingTV: getVal('streamingTV'),
        StreamingMovies: 0,
        PaperlessBilling: getVal('paperlessBilling'),
        MonthlyCharges: getFloat('monthlyCharges'),
        TotalCharges: getFloat('totalCharges'),
        InternetService: getVal('internetService'),
        Contract: getVal('contract'),
        PaymentMethod: getVal('paymentMethod')
    };

    // लोडिंग इफेक्ट दिखाने के लिए (वैकल्पिक)
    document.getElementById('churnResult').innerText = "Processing...";
    document.getElementById('resultBox').style.display = 'block';

    try {
        // 3. FastAPI को POST रिक्वेस्ट भेजें
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
         // पॉप-अप दिखाएं
const modal = document.getElementById('predictionModal');
const modalChurn = document.getElementById('modalChurn');
const modalProb = document.getElementById('modalProb');

modalChurn.innerText = result.churn;
modalProb.innerText = result.probability;
modalChurn.style.color = (result.churn === "Yes") ? "red" : "green";

modal.style.display = "block"; // पॉप-अप खोलें

        // 4. रिजल्ट को स्क्रीन पर अपडेट करें
        document.getElementById('churnResult').innerText = result.churn;
        document.getElementById('probResult').innerText = result.probability;

        // रिजल्ट के हिसाब से रंग बदलना (Yes के लिए लाल, No के लिए हरा)
        if(result.churn === "Yes") {
            document.getElementById('churnResult').style.color = "red";
        } else {
            document.getElementById('churnResult').style.color = "green";
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Prediction failed. Please check the console or ensure the server is running.');
        document.getElementById('resultBox').style.display = 'none';
    }
}

// पॉप-अप बंद करने का फंक्शन
function closeModal() {
    document.getElementById('predictionModal').style.display = "none";
}

function resetForm() {
    // 1. पूरे फॉर्म को रीसेट करना
    document.getElementById('predictionForm').reset();
    
    // 2. पुराने रिज़ल्ट बॉक्स को छिपाना
    document.getElementById('resultBox').style.display = 'none';
    
    // 3. साफ़ फीडबैक के लिए कंसोल में लॉग (वैकल्पिक)
    console.log("Form and results have been reset.");
}
