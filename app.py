from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load Gemini Flash 1.5 model & get response
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
chat = model.start_chat(history = [])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Initialise our Streamlit app
st.set_page_config (page_title = "Gemo Chatbot")
st.header("Gemo")


# Initialise session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input : ", key = "input")


# Create columns for the buttons
col1, col2, col3 = st.columns([0.4, 1, 0.4])

with col1:
    submit = st.button("Ask the question")
with col2:
    clear_history = st.button("Clear Chat History")


if submit and input:
    response = get_gemini_response(input)
    # Add user query & response to session chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is.....")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))


if clear_history:
    st.session_state['chat_history'] = []


with st.expander("The Chat history is..."):
    for role,text in st.session_state['chat_history']:
        st.write(f"{role}:{text}")
