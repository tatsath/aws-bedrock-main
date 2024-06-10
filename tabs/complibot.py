import streamlit as st
import chatbot_backend as demo

def display():
    st.header("Complibot")
    st.write("Meet Complibot, your virtual compliance assistant. Ask Complibot any compliance-related questions and get instant, accurate answers. Whether it's about regulatory changes or compliance best practices, Complibot is here to help.")

    # with st.chat_message("user"):
    #     st.write("Hello 👋")

    # Example chatbot interaction
    #user_input = st.text_input("Ask Complibot a question:")
    #if user_input:
    
    if 'memory' not in st.session_state:
        st.session_state.memory = demo.demo_memory()

    # add chat history to session
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # render chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    # input text box for chatbot
    input_text = st.text_input("Ask Complibot a question:")
    #input_text = st.chat_input("Type your question here")
    #st.write(f"Complibot: Here is the response to your question '{input_text}'")

    if input_text:
        with st.chat_message("user"):
            st.markdown(input_text)

        # Append user input to chat history
        st.session_state.chat_history.append({"role":"user", "text":input_text})

        # Generate chat response using the chatbot instance
        chat_response = demo.demo_conversation(input_text=input_text, memory=st.session_state.memory)

        # Display the chat response
        with st.chat_message("assistant"):
            st.markdown(chat_response["response"])

        # Append assistant's response to chat history
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response["response"]})
        
            