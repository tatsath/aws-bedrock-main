import streamlit as st
from langchain.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import boto3
import appChat as appFile
from langchain.prompts import PromptTemplate

# Function to display compliance reasons

bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)


prompt_template_compliance = """
Imagine you are a compliance officer for a bank checking if policies and guidelines are being met.
Check the sections of the following document on whether the policies are being met.
<question>
{question}
</question

The following are the poilicies to be checked against:
<context>
{context}
</context

Provide the reason for non compliance with the corresponding section of the document 
and suggest edits to be made. Be as granular as possible. Provide just the summary of the non-compliant sections 
and a high level yes, no or partially compliant
in form of table with the section in one column, yes or no in the other column and the high level reason of non 
compliance or partial compliance in less than 10 words. 
Add the detailed summary under the table with the non compliant or partially compliant sections with quoted reference and 
suggested change. 
Please refer only to the document. 
Please be formal in your response. 
Please avoid any biases.
Assistant:"""

PROMPT1 = PromptTemplate(
    template=prompt_template_compliance, input_variables=["context", "question"]
)

def compliance_reasons(section):
    reasons = {
        "Introduction": "Compliant because...",
        "Scope": "Not approved because...",
        "Governance": "Partially approved because...",
        "Risk Management": "Compliant because..."
    }
    st.write(reasons[section])

def display():
    st.header("CompliCheck")
    st.write("CompliCheck is your go-to solution for all compliance checks. Simply upload your documents, and our advanced AI will analyze and ensure that all regulatory requirements are met. Stay compliant with ease and confidence.")

    # Example upload widget
    uploaded_file = st.file_uploader("✍️ Upload your compliance document")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        user_question = appFile.extract_pdf(uploaded_file)    

           

    option = st.selectbox(
    "🏆 Choose the guidelines to check against",
    ("FINRA", "BIA", "Regulatory", "External Audit", "Legal and Compliance"))

    #if option == "BIA" and uploaded_file is not None:

    if option == "FINRA":
        with st.spinner("Processing..."):
            print('in FINRA')            
            faiss_index = FAISS.load_local("VectorDB/faiss_index_finra", bedrock_embeddings, allow_dangerous_deserialization=True)
            print('faiss_index populated')
            # llm=get_claude_llm()
            # if user_question is not None:
            # #document = extract_pdf(uploaded_file)
            #     st.write(get_response_llm(llm,faiss_index,user_question, PROMPT1))

    if option == "BIA":
        with st.spinner("Processing..."):
            print('in BIA')            
            faiss_index = FAISS.load_local("VectorDB/faiss_index_bia", bedrock_embeddings, allow_dangerous_deserialization=True)
            print('faiss_index populated')
            llm=appFile.get_claude_llm()
            # if user_question is not None:
            document = appFile.extract_pdf(uploaded_file)
            st.write(appFile.get_response_llm(llm,faiss_index,user_question, PROMPT1))
            st.success("Done")


            #     st.success("Done")

    if option == "Regulatory":
        with st.spinner("Processing..."):
            print('in Regulatory')            
            faiss_index = FAISS.load_local("VectorDB/faiss_index_regulatory", bedrock_embeddings, allow_dangerous_deserialization=True)
            print('faiss_index populated')
            # llm=get_claude_llm()
            # if user_question is not None:
            # #document = extract_pdf(uploaded_file)
            #     st.write(get_response_llm(llm,faiss_index,user_question, PROMPT1))
            #     st.success("Done")     
    
    if option == "External Audit":
        with st.spinner("Processing..."):
            print('in External Audit')            
            faiss_index = FAISS.load_local("VectorDB/faiss_index_extaudit", bedrock_embeddings, allow_dangerous_deserialization=True)
            print('faiss_index populated')
            # llm=get_claude_llm()
            # if user_question is not None:
            # #document = extract_pdf(uploaded_file)
            #     st.write(get_response_llm(llm,faiss_index,user_question, PROMPT1))
            #     st.success("Done")   
          
    if option == "Legal and Compliance":
        with st.spinner("Processing..."):
            print('in Legal and Compliance')            
            faiss_index = FAISS.load_local("VectorDB/faiss_index_legalcomp", bedrock_embeddings, allow_dangerous_deserialization=True)
            print('faiss_index populated')
            # llm=get_claude_llm()
            # if user_question is not None:
            # #document = extract_pdf(uploaded_file)
            #     st.write(get_response_llm(llm,faiss_index,user_question, PROMPT1))
            #     st.success("Done")   
    
    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='header table'>My Doc</div>", unsafe_allow_html=True)
        with st.container():
            for section in ["Introduction", "Scope", "Governance", "Risk Management"]:
                with st.expander(section):
                    st.write(f"{section} details...")
                    st.write("**Accept CompliEase change?**")
                    st.radio(f"Accept CompliEase change for {section}?", ["Yes", "No"], index=0, key=f"{section}_choice")

    with col2:
        st.markdown("<div class='header-compliance table'>Am I compliant?</div>", unsafe_allow_html=True)
        compliance_status = {
            "Introduction": "Good",
            "Scope": "Don't approve",
            "Governance": "Partially approve",
            "Risk Management": "Good"
        }
        status_colors = {
            "Good": "background-color: lightgreen; color: black;",
            "Don't approve": "background-color: lightcoral; color: black;",
            "Partially approve": "background-color: lightyellow; color: black;"
        }

        with st.container():
            for section, status in compliance_status.items():
                with st.expander(f"{section}: {status}"):
                    st.markdown(f"<div class='status' style='{status_colors[status]}'>{section}: {status}</div>", unsafe_allow_html=True)
                    compliance_reasons(section)
