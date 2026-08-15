import streamlit as st
from groq import Groq
import os

# Use a secure way to handle keys (like st.secrets or env variables)
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your-api-key-here"))

st.sidebar.title("Settings")
temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.7)  # Fixed slider range (max 1.0)
style = st.sidebar.selectbox("Response Style", ["Simple", "Detailed", "Professional"])

system_prompt = f"You are a helpful assistant. Explain things in a {style} way in English."
model_id = "openai/gpt-oss-120b"

# Initialize session state for history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

st.title("Chatbot with Groq LLM")

# Display chat history from session state
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User Input
if user_input := st.chat_input("Ask Anything:"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=st.session_state.messages,
            temperature=temperature,
        )

        full_response = response.choices[0].message.content

        # Add AI response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        with st.chat_message("assistant"):
            st.markdown(full_response)

    except Exception as e:
        st.error(f"An error occurred: {e}")