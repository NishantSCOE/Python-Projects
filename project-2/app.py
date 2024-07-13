from dotenv import load_dotenv
import os
 
load_dotenv()  # take environment variables from .env.

import streamlit as st
from PIL import Image
import google.generativeai as genai

# Loading Google API Key from .env file
api_key = os.getenv("GOOGLE_API_KEY")


def get_gemini_response(input_text, image, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {"mime_type": uploaded_file.type, "data": bytes_data}
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

favicon_path = 'star.ico'  # Replace with your actual path or URL
st.set_page_config(page_title="Gemini Invoice Analyzer", page_icon=favicon_path, layout="wide")

st.title("Gemini Invoice Analyzer")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload and Analyze")
    st.markdown("---")  # Horizontal line for separation
    input_text = st.text_input("Input Prompt: ", key="input")
    submit = st.button("Analyze Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

with col2:
    st.subheader("Analysis Result")
    st.markdown("---")  # Horizontal line for separation
    if submit:
        if uploaded_file is not None:
            try:
                image_data = input_image_setup(uploaded_file)
                input_prompt = "You are an expert in understanding invoices. You will receive input images as invoices & you will have to answer questions based on the input image."
                with st.spinner("Analyzing the invoice..."):
                    response = get_gemini_response(input_text, image_data, input_prompt)
                    st.write(response)
            except FileNotFoundError as e:
                st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
        else:
            st.error("Please upload an image to analyze.")
