import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client - NEW SYNTAX
api_key = os.getenv("OPENAI_API_KEY")
st.sidebar.write(f"API Key loaded: {bool(api_key)}")
st.sidebar.write(f"Key starts with: {api_key[:7] if api_key else 'None'}")

if not api_key:
    st.error("❌ API key not found! Check your .env file")
else:
    client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stChatInput { position: fixed; bottom: 20px; width: 80%; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    model = st.selectbox("Choose model:", ["gpt-3.5-turbo", "gpt-4"])
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.7)

st.title("🤖 AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display chat messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # NEW OpenAI v1.0.0+ syntax
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    max_tokens=500,
                    temperature=temperature
                )
                
                bot_response = response.choices[0].message.content
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                st.error(f"Error: {e}")

