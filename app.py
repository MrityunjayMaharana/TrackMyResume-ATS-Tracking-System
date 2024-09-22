from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, pdf_content, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images using Poppler
        images = pdf2image.convert_from_bytes(uploaded_file.read(), dpi=200, poppler_path='C:\\Program Files (x86)\\poppler\\Library\\bin')
        first_page = images[0]
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Show the image on the Streamlit app
        st.image(first_page, caption='First Page of the Resume', use_column_width=True)

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("TrackMyResume - ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Suggestions to Improve Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Additional Insights")

# Define prompts for each submit button
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced Career Advisor. Based on the provided resume and job description, suggest specific skills or experiences the candidate should improve upon.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage of match if the resume matches
the job description. First, output the percentage, then list the missing keywords, and finally, share your final thoughts.
"""

input_prompt4 = """
You are an expert in professional development. Analyze the resume and provide additional insights on how the candidate can enhance their profile 
for better job opportunities.
"""

if submit1:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif submit2:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif submit4:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt4, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
