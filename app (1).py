import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI  # Import ChatOpenAI instead of OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Load the dataset
file_name = 'Bowling_Personal_Data.xlsx'
try:
    df = pd.read_excel(file_name)
except FileNotFoundError:
    st.error("Error: Bowling_Personal_Data.xlsx not found. Please ensure the data file is in the correct directory.")
    st.stop()

# Define the prompt template for LangChain
prompt_template = """
You are an expert bowling coach. Analyze the provided bowling data, which includes player names,
throw speeds, throw heights, and pins hit. Based on this data, offer bowling advice
to improve a player's performance.

Data:
{data}

The player is {player}. Their throw speed is {speed} m/s, and their throw height is {height} m.

Provide specific, actionable advice based on the data, focusing on how the player might adjust their technique
to improve their score. Consider factors such as optimal speed, height, and any patterns in the data.
"""

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Initialize memory
memory = ConversationBufferMemory()

# Initialize LangChain
prompt = PromptTemplate.from_template(prompt_template)
llm_chain = LLMChain(prompt=prompt, llm=llm, memory=memory)

# Streamlit app
st.title("Bowling Advice Chatbot")

# Text input for user prompt
user_prompt = st.text_area("Enter your bowling question or request:")

# Chatbot interaction
if st.button("Get Advice"):
    if not user_prompt:
        st.warning("Please enter a prompt.")
    else:
        # Format the prompt with the user's input and data
        prompt_text = f"You are an expert bowling coach. Analyze the provided bowling data, which includes player names, throw speeds, throw heights, and pins hit. Based on this data, and the user's prompt, offer bowling advice. Data: {df.to_string()}. User's prompt: {user_prompt}"

        # Get the advice from LangChain using ChatOpenAI
        response = llm.predict(prompt_text)
        st.write(f"Advice: {response}")