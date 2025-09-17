import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stChatInput {
        position: fixed;
        bottom: 20px;
        width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    model = st.selectbox(
        "Choose model:",
        ["gpt-3.5-turbo", "gpt-4"]
    )
    temperature = st.slider("Temperature:", 0.0, 1.0, 0.7)

# Main content
st.title("🤖 AI Chatbot")
st.write("Chat with OpenAI's powerful AI models!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Display chat messages
for message in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=st.session_state.messages,
                    max_tokens=500,
                    temperature=temperature
                )
                
                bot_response = response.choices[0].message['content']
                st.markdown(bot_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
            except Exception as e:
                st.error(f"Error: {e}")