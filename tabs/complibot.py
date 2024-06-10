import streamlit as st

def display():
    st.header("Complibot")
    st.write("Meet Complibot, your virtual compliance assistant. Ask Complibot any compliance-related questions and get instant, accurate answers. Whether it's about regulatory changes or compliance best practices, Complibot is here to help.")

    with st.chat_message("user"):
        st.write("Hello 👋")

    # Example chatbot interaction
    user_input = st.text_input("Ask Complibot a question:")
    if user_input:
        st.write(f"Complibot: Here is the response to your question '{user_input}'")
