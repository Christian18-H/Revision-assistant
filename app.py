import streamlit as st
import os
import google.generativeai as genai

# Gemini API Key (replace with your real key or use environment variable)
GEMINI_API_KEY = "AIzaSyDVLjmWaDUyAfgY7RIqFmlUfqObrev5zAk"
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Function to call Gemini SDK
def analyze_results(patient_data):
    prompt = f"""
    A doctor has uploaded the following patient test results:

    {patient_data}

    Analyze the results and give a short summary with possible medical conditions (if any),
    and recommend follow-up actions or advice to the patient.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

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
