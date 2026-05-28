import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import re

# Database Connection
conn = sqlite3.connect("health.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()

# Prediction Function
def predict_health(glucose, haemoglobin, cholesterol):

    if glucose > 140 and cholesterol > 240:
        return "High risk of diabetes and cholesterol issues"

    elif haemoglobin < 12:
        return "Possible anemia risk"

    elif glucose > 125:
        return "Possible diabetes risk"

    else:
        return "Normal health indicators"

# Email Validation
def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# App Title
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>
    🏥 Health Prediction Application
    </h1>
    <hr>
    """,
    unsafe_allow_html=True
)
st.write(
    "AI-powered healthcare prediction system using Python and Streamlit"
)
# Sidebar
menu = st.sidebar.selectbox(
    "Menu",
   ["Add Patient", "View Patients", "Update Patient", "Delete Patient"]
)

# ---------------- ADD PATIENT ---------------- #

if menu == "Add Patient":

    st.subheader("Add Patient Record")

    full_name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1900,1,1),
        max_value=date.today()
    )

    email = st.text_input("Email Address")

    glucose = st.number_input("Glucose", min_value=0.0)

    haemoglobin = st.number_input("Haemoglobin", min_value=0.0)

    cholesterol = st.number_input("Cholesterol", min_value=0.0)

    if st.button("Save Record"):

        # Validation
        if full_name == "":
            st.error("Full Name is required")

        elif not valid_email(email):
            st.error("Enter valid email address")

        else:

            remarks = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            cursor.execute("""
            INSERT INTO patients (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                full_name,
                str(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            ))

            conn.commit()

            st.success("Patient record saved successfully!")

            st.write("Prediction Result:")
            st.info(remarks)

# ---------------- VIEW PATIENTS ---------------- #

elif menu == "View Patients":

    st.subheader("Patient Records")

    cursor.execute("SELECT * FROM patients")

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        "ID",
        "Full Name",
        "DOB",
        "Email",
        "Glucose",
        "Haemoglobin",
        "Cholesterol",
        "Remarks"
    ])

    st.dataframe(df)

# ---------------- UPDATE PATIENT ---------------- #

elif menu == "Update Patient":

    st.subheader("Update Patient Record")

    patient_id = st.number_input(
        "Enter Patient ID to Update",
        min_value=1,
        step=1
    )

    if st.button("Load Record"):

        cursor.execute(
            "SELECT * FROM patients WHERE id=?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient:

            st.session_state.patient = patient

        else:
            st.error("Patient not found")

    if "patient" in st.session_state:

        patient = st.session_state.patient

        full_name = st.text_input(
            "Full Name",
            value=patient[1]
        )

        email = st.text_input(
            "Email",
            value=patient[3]
        )

        glucose = st.number_input(
            "Glucose",
            value=float(patient[4])
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            value=float(patient[5])
        )

        cholesterol = st.number_input(
            "Cholesterol",
            value=float(patient[6])
        )

        if st.button("Update Record"):

            remarks = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            cursor.execute("""
            UPDATE patients
            SET
                full_name=?,
                email=?,
                glucose=?,
                haemoglobin=?,
                cholesterol=?,
                remarks=?
            WHERE id=?
            """, (
                full_name,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                patient_id
            ))

            conn.commit()

            st.success("Patient updated successfully!")
        st.info(remarks)
            # ---------------- DELETE PATIENT ---------------- #

elif menu == "Delete Patient":

    st.subheader("Delete Patient Record")

    patient_id = st.number_input(
        "Enter Patient ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Record"):

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()

        st.success("Record deleted successfully!")