import streamlit as st
import os
from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.docstore.document import Document
load_dotenv()
api_key = os.getenv("openai_api_key")
def job_description_resume(prompt):
   llm = OpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo-instruct", max_tokens=3000)
   llm_chain = LLMChain(prompt=prompt, llm=llm)
   return llm_chain.invoke({})
   
# st.title("Build your Resume")
st.subheader("Tailor Your Resume", divider='rainbow')
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])
job_description  = st.text_area("Job Description:","Paste the job description here that you'd like to tailor your resume to")
prompt = st.text_area("Prompt:","For the given job description and resume text below, please modify my resume text in such way that resume text and job description are 90% matched")
if uploaded_file is not None:
  st.success("File uploaded successfully!")
  # try:
  reader = PdfReader(uploaded_file)
  resume_string = ""
  i = 1
  for page in reader.pages:
      resume_string += page.extract_text()
      i += 1
  # except Exception as e:
  #    print("File load exception!")
button = st.button("Generate")
if button and prompt and job_description and resume_string: 
    with st.spinner("Generating Answer"):
        prompt_template = PromptTemplate.from_template(
        prompt+"\n\n"+"Job_description:"+job_description+"\n\n"+"Resume_text:"+resume_string
        )
        resp = job_description_resume(prompt_template)
    st.write(resp)