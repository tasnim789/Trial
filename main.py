import streamlit as st
from transformers import pipeline
import torch

# Page configuration
st.set_page_config(
    page_title="🤖 Free AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Free AI Chatbot")
st.write("💡 No API keys or external tools needed!")

# Load a small local model
@st.cache_resource
def load_model():
    try:
        return pipeline(
            "text-generation",
            model="gpt2",
            device=-1,  # Use CPU
            max_length=100,
            torch_dtype=torch.float32
        )
    except:
        return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
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
                model = load_model()
                if model:
                    response = model(prompt, max_length=100)[0]['generated_text']
                    # Clean up response
                    response = response.replace(prompt, "").strip()
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.info("💡 First time setup: Downloading AI model... This may take a minute.")
            except Exception as e:
                st.error(f"Error: {e}")

# Instructions
with st.sidebar:
    st.title("ℹ️ Instructions")
    st.write("""
    This chatbot uses GPT-2 running locally on your device.
    
    **First run might take a minute** to download the model.
    
    No internet required after initial download!
    """)
