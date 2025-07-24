import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini Flash 1.5 model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="🎓 Gemini Academic Explorer", layout="wide")
st.title("🎓 Gemini Flash 1.5 Academic Data Explorer")

uploaded_file = st.file_uploader("📤 Upload CSV or Excel", type=["csv", "xlsx"])

df = None
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("✅ File loaded successfully!")

        st.subheader("📊 Data Preview")
        st.dataframe(df.head(), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

if df is not None:
    st.subheader("🧠 Ask Gemini about your data")
    user_query = st.text_input("Type your question (e.g. 'Top 5 students by GPA')")

    if st.button("Ask Gemini") and user_query:
        with st.spinner("💬 Gemini is thinking..."):
            prompt = f"""You are an academic data analyst. Analyze the dataset below and answer the question:

DATA:
{df.head(20).to_csv(index=False)}

QUESTION:
{user_query}
"""
            try:
                response = model.generate_content(prompt)
                st.success("✅ Gemini's Answer")
                st.write(response.text)
            except Exception as e:
                st.error(f"⚠️ Gemini Error: {e}")
