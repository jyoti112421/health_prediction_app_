# Health Prediction Application

## Project Overview
This is an AI-powered healthcare prediction system built using Python, Streamlit, and SQLite.

The application allows users to:
- Add patient records
- View patient records
- Update patient records
- Delete patient records
- Predict possible health risks based on medical values

---

## Features
- CRUD Operations
- SQLite Database Integration
- AI Prediction Logic
- Email Validation
- Streamlit User Interface
- Persistent Data Storage

---
## Prediction Model

The application uses a custom rule-based prediction model to generate possible health risk predictions based on blood test values including glucose, haemoglobin, and cholesterol.

---

## Technologies Used
- Python
- Streamlit
- SQLite
- Pandas

---

## How to Run the Project

### Install Dependencies
pip install -r requirements.txt

### Run Application
python -m streamlit run app.py

---

## Prediction Logic
The system predicts:
- Diabetes Risk
- Cholesterol Issues
- Anemia Risk
- Normal Health Indicators

based on:
- Glucose
- Haemoglobin
- Cholesterol

## Live Demo
- https://health-prediction-app.streamlit.app
