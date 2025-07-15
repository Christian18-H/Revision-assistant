import streamlit as st
import os
import json
import requests

# Your Gemini API Key
API_KEY = "AIzaSyDVLjmWaDUyAfgY7RIqFmlUfqObrev5zAk"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY

# Function to call Gemini API
def analyze_results(patient_data):
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
    A doctor has uploaded the following patient test results:

    {patient_data}

    Analyze the results and give a short summary with possible medical conditions (if any),
    and recommend follow-up actions or advice to the patient.
    """

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        output = response.json()
        return output["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="AI Medical Assistant", layout="centered")
st.title("🩺 AI Medical Assistant")

st.write("Upload patient results (e.g., lab reports, symptoms, etc.) in text format.")

uploaded_file = st.file_uploader("Upload Medical Report", type=["txt"])

if uploaded_file is not None:
    patient_data = uploaded_file.read().decode("utf-8")
    st.subheader("📄 Patient Report")
    st.text_area("Uploaded Data", value=patient_data, height=300)

    if st.button("Analyze & Recommend"):
        with st.spinner("Analyzing..."):
            response = analyze_results(patient_data)
        st.subheader("🧠 AI Recommendation")
        st.markdown(response)
