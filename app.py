from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import io
import os
from PIL import Image
import pdf2image
import base64
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def gemini_response(input, pdf_content, prompt):
    ## Define the generative model to be used
    ##https://ai.google.dev/gemini-api/docs/models/gemini#:~:text=Gemini%20is%20a%20family%20of,fit%20for%20your%20use%20case.
    model = genai.GenerativeModel(model_name= "gemini-pro-vision")
    response = model.generate_content(contents = [input, pdf_content[0], prompt])
    return response.text

#Converting pdf to image
def input_pdf_setup(uploaded_file):
    ## Check if the uploaded file is present
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(pdf_file = uploaded_file.read())

        first_pg = images[0]

        ## Convert to bytes
        img_byte_arr = io.BytesIO()
        first_pg.save(img_byte_arr, format = "JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else: raise FileNotFoundError("Please Upload the File")

## Streamlit App

st.set_page_config(page_title = "Gemini Resume Expert")
st.header("Application Tracking System - ATS")

## Provide the job description
input_text = st.text_area(label = "Job Description", key = "input")

uploaded_file = st.file_uploader(label = "Upload Your Resume (Only Pdf)", 
                                 type = ["pdf"])
if uploaded_file is not None:
    st.write("File Uploaded Successfully!!")


## Prompts
submit1 = st.button("Keypoints in my Resume")
submit2 = st.button("Match with Job Description")
submit3 = st.button("Keywords Missing in the Resume based on Job Description")


sub1_prompt1 = "Extract technical skills, soft skills, education details, and experience/project information directly from the resume. Only include information explicitly stated in the resume for each category."

sub2_prompt2 = "Given a resume and a job description, generate a table illustrating the match. Use cues to represent high, medium, and low match areas, highlighting strengths and weaknesses."

sub3_prompt3 = "Analyze a resume and job description. Identify keywords and skills from the job description absent in the resume. Prioritize based on frequency and relevance to the job. Provide suggestions for integrating these keywords into the resume, emphasizing achievements and quantifiable results."

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = gemini_response(sub1_prompt1, pdf_content,input_text)
        st.subheader("Highlights of your resume: ")
        st.write(response)

    else:
        st.write("Please Upload the Pdf Resume!!!")

elif submit2:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = gemini_response(sub2_prompt2, pdf_content,input_text)
            st.subheader("JD vs Your Resume: ")
            st.write(response)

        else:
            st.write("Please Upload the Pdf Resume!!!")

else:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = gemini_response(sub3_prompt3, pdf_content,input_text)
        st.subheader("Increase the chance of hiring with these keywords: ")
        st.write(response)

    else:
        st.write("Please Upload the Pdf Resume!!!")
















