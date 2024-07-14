import streamlit as st
import requests  # For making API calls to your backend

# Replace with the URL of your backend service
BACKEND_URL = "http://localhost:8502"  

def upload_and_answer(file_path, question, answer_options):
  """Uploads document, question and options to backend and returns answer"""
  data = {
      "file_path": file_path,
      "question": question,
      "answer_options": answer_options
  }
  response = requests.post(BACKEND_URL, json=data)
  if response.status_code == 200:
      return response.json()["answer"]
  else:
      return f"Error: {response.text}"  # Handle potential errors from backend

st.title("Ollama Question Answering")

uploaded_file = st.file_uploader("Upload a PDF document")

if uploaded_file is not None:
  question = st.text_input("Enter your question")
  answer_options = st.multiselect("Provide answer options (optional)", [])
  
  if st.button("Submit"):
      # Read uploaded file content
      file_content = uploaded_file.read()
      
      # Save the uploaded file temporarily (optional, adjust path as needed)
      with open("temp_file.pdf", "wb") as f:
          f.write(file_content)
      file_path = "temp_file.pdf"  # Adjust path if saved elsewhere
      
      answer = upload_and_answer(file_path, question, answer_options)
      st.write(f"Answer: {answer}") 
      
      # Clean up temporary file (optional)
      # os.remove("temp_file.pdf")
else:
  st.info("Upload a PDF document to get started.")
