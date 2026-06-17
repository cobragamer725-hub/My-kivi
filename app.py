import streamlit as st
import google.generativeai as genai

# 1. Set up the web page look and feel
st.set_page_config(page_title="My AI Web App", page_icon="🤖", layout="centered")

st.title("🤖 Mama AI")
st.write("Type your prompt below to talk to the AI model.")
st.divider()

# 2. Securely handle your Gemini API Key
# (We will set this up in the Streamlit Dashboard in the next step)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Gemini API Key is missing! Please add it to your Streamlit Secrets.")
else:
    # Configure the AI model with your key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 3. Create the user interface
    user_prompt = st.text_area(
        "What is on your mind?", 
        placeholder="Ask me anything...",
        height=120
    )

    # 4. Run the AI logic when the button is clicked
    if st.button("Ask AI", type="primary"):
        if user_prompt.strip() == "":
            st.warning("Please type something first!")
        else:
            with st.spinner("Thinking..."):
                try:
                    # Send the text to the Gemini AI model
                    response = model.generate_content(user_prompt)
                    
                    # Display the answer on the website
                    st.success("Done!")
                    st.subheader("AI Response:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# Sidebar info
st.sidebar.title("App Status")
st.sidebar.success("Web Server: Live 🟢")
