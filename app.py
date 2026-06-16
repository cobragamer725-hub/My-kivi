import streamlit as st
import google.generativeapi as genai

# Configure the API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# This was the line causing the 429 quota/timer error because it used the 2.5-flash model
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Ankit Mandal AI")
st.write("Type your prompt below to talk to the AI model.")

# The old text input and button setup
user_input = st.text_input("What is on your mind?", key="user_prompt")

if st.button("Ask AI"):
    if user_input:
        try:
            # Sending a single isolated request every time the button was clicked
            response = model.generate_content(user_input)
            st.write(response.text)
        except Exception as e:
            # This is where the 429 / 404 error messages were caught and displayed
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt.")

