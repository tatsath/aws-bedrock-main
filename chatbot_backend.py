# import modules
import os
import boto3
from langchain.llms.bedrock import Bedrock
#from langchain_anthropic import AnthropicLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain_community.chat_models.bedrock import BedrockChat
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

bedrock=boto3.client(service_name="bedrock-runtime")

# function that invokes bedrock model
""" def demo_chatbot():
    demo_llm = Bedrock(
        credentials_profile_name="default",
        model_id="meta.llama2-70b-chat-v1",
        model_kwargs={
            "temperature": 0.9,
            "top_p": 0.5,
            "max_gen_len": 512
        }
    )
    return demo_llm """

def demo_chatbot():
    demo_llm = Bedrock(
        credentials_profile_name="default",
        model_id="anthropic.claude-v2:1",
        model_kwargs={
            "temperature": 0.9,
            "top_p": 0.5,
            "max_tokens_to_sample": 512
        }
    )
    return demo_llm

def get_claude_llm():
    ##create the Anthropic Model
    llm=BedrockChat(model_id="anthropic.claude-3-sonnet-20240229-v1:0",client=bedrock,
                model_kwargs={'max_tokens':500})
    
    return llm



# function for conversation memory
def demo_memory():
    llm_data = demo_chatbot()
    memory = ConversationBufferMemory(
        llm=llm_data,
        max_token_limit=512
    )
    return memory

# function for conversation
def demo_conversation(input_text, memory):
    llm_chain_data = demo_chatbot()
    llm_conversation = ConversationChain(
        llm=llm_chain_data,
        memory=memory,
        verbose=True
    )        

# chat response using invoke (prompt template)
    chat_reply = llm_conversation.invoke(input=input_text)
    return chat_reply

def generate_response(uploaded_file, llm, query_text):
    # Load document if file is uploaded
    if uploaded_file is not None:
        documents = uploaded_file
        #documents = [uploaded_file.read().decode()]
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        #embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)
        # Create a vectorstore from documents
        #db = Chroma.from_documents(texts, embeddings)
        db=FAISS.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        #qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        return qa.run(query_text)