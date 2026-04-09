import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Better than Chatgpt",
    page_icon="😊",
    layout="centered",
)
st.title("😊Better than Chatgpt")
st.caption("A chatbox powered by Groq API - built with Python+ Streamlit , Prepared By Atharv Agrawal")

with st.sidebar:
    st.header("Setup")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at https://console.groq.com",
    )

    model = st.selectbox(
        "Model",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        help="All models are free on Groq!"
    )
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

    st.markdown("""
    **How to get a free API Key:**
     1. Go to [console.groq.com](https://console.groq.com)
     2.Sign up/ Log in
     3. Click **API keys - Create Key**
     4. Paste it above                                    
     """)
    
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    # guard: check api key is set
    if not api_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()
    # 1. show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    # 2. call Groq API
    client = Groq(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Groq is thinking..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    *st.session_state.messages,
                ],
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})