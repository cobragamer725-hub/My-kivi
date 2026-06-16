import streamlit as st
import google.generativeapi as genai

# 1. Setup the Free AI Connection
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# 2. Make the page look like a real Chat App
st.set_page_config(page_title="Gemini AI", page_icon="💬")
st.title("💬 Ankit Mandal AI")

# 3. Create persistent chat memory inside the app
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Render the existing chat bubble history on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The modern input bar pinned at the bottom
if prompt := st.chat_input("Message Gemini..."):
    
    # Display what you just typed inside a user chat bubble
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from the AI using the free tier safely
    try:
        response = st.session_state.chat_session.send_message(prompt)
        
        # Display Gemini's response inside an assistant bubble
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        if "429" in str(e):
            st.error("⏱️ Google's free tier limit reached. Wait 10 seconds before typing your next prompt!")
        else:
            st.error(f"An error occurred: {e}")
            
