🚀 Customer Churn Prediction System
This is an End-to-End Machine Learning web application designed to predict whether a customer is likely to leave a service (churn). The project features a high-performance backend built with FastAPI and a modern, responsive frontend crafted using HTML5, CSS3, and Vanilla JavaScript.
🛠 Tech Stack
Backend: FastAPI (Python)
Machine Learning: Scikit-learn (Random Forest Classifier), Pickle
Frontend: HTML5, CSS3, JavaScript (Fetch API)
Web Server: Uvicorn
🌟 Key Features
Real-time Prediction: Get instant results without refreshing the page thanks to asynchronous API calls.
Interactive UI: A clean and modern design featuring smooth CSS animations and depth-defining shadows.
Professional Modal Pop-up: Prediction results are displayed in a stylish overlay for better user focus.
Dynamic Result Coloring: The UI automatically highlights "Churn" in red and "No Churn" in green for quick visual analysis.
Form Reset Functionality: A dedicated reset button to clear all inputs and previous results instantly for new testing.
Mobile Responsive: A fluid layout that adjusts perfectly to desktops, tablets, and smartphones.

📂 Project Structure
├── model/
│   └── random_forest_model.pkl   # Pre-trained Machine Learning model
├── static/
│   ├── css/
│   │   └── style.css            # Custom styling and animations
│   └── js/
│       └── script.js            # API communication and UI logic
├── templates/
│   └── index.html               # Main User Interface (Dashboard)
├── main.py                      # FastAPI server routes and model logic
└── README.md

🚀 Installation & Setup
1. Prerequisites
Ensure you have Python 3.8+ installed. Install the required dependencies using pip:
    pip install fastapi uvicorn scikit-learn pandas
    
2. Run the Application
Navigate to the project root directory and start the Uvicorn server:
    uvicorn main:app --reload
    
3. Access the Web App
Open your browser and navigate to:
http://127.0.0.1:8000
⚙️ API Endpoints
GET /: Renders and serves the main HTML dashboard.
POST /predict: Accepts customer data in JSON format and returns the churn prediction and probability.
GET /docs: Access the interactive Swagger UI documentation provided by FastAPI.
📝 How To Use
Input Data: Enter the customer details such as Tenure, Monthly Charges, Contract type, etc., into the form.
Predict: Click the 'Predict Churn' button.
View Result: A modal will pop up displaying the Churn status (Yes/No) and the calculated probability.
Test Again: Use the 'Reset Form' button to clear all fields for a fresh prediction.
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
Developed with ❤️ by Sachin Tewari 
My youtube channel url : https://www.youtube.com/@dc_1136
