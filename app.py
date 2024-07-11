from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set your GOOGLE_API_KEY in the .env file.")

def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit Application Setup
st.set_page_config(page_title="Gemini Q&A", layout="centered")

st.title("Gemini Q&A Application")

input_text = st.text_input("Enter your question here:")

if st.button("Ask the Question"):
    if input_text:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.error("Please enter a question.")
