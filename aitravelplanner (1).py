# -*- coding: utf-8 -*-
import subprocess
import os
import streamlit as st
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Install necessary packages
subprocess.run(["pip", "install", "--upgrade", "pip"])
subprocess.run(["pip", "install", "langchain", "langchain_google_genai", "google-generativeai", "streamlit"])

# ✅ Output Parser
output_parser = JsonOutputParser()
format_instructions = """
Output a JSON object in the following format:
{
    "travel_options": [
        {"mode": "bus", "cost": "$50", "duration": "5h"},
        {"mode": "train", "cost": "$30", "duration": "3h"},
        {"mode": "flight", "cost": "$120", "duration": "1h"}
    ]
}
"""

# ✅ Chat Prompt Template
prompt_template = ChatPromptTemplate(
    messages=[
        (
            "system", """You are an AI-powered travel assistant. Your task is to find the best travel options from {source} to {destination}.
            Provide a minimum of three travel options, including:
            - **Road**: Cab, Bus
            - **Rail**: Train
            - **Air**: Flight
            Include: Mode, Cost, Duration in **JSON format**.
            {format_instructions}
            """
        ),
        (
            "human", """I want to travel from {source} to {destination}.
            Modes of transport: {mode}.
            Provide at least three options in **JSON format**.
            {format_instructions}
            """
        )
    ],
    partial_variables={"mode": "Flight"}
)

# ✅ Set up Gemini API Key
gemini_api_key = "AIzaSyDT_I6RfdL2Chd6Y4ceQa-b2kPLpjHvbWM" 

chat_model = ChatGoogleGenerativeAI(google_api_key=gemini_api_key, model="gemini-2.0-flash-exp")
chain = prompt_template | chat_model | output_parser

# ✅ Streamlit UI
st.title("✈️ AI Travel Assistant")

source = st.text_input("Leaving From:")
destination = st.text_input("Destination:")
mode_options = ["Flight", "Train", "Bus", "Cab"]
mode = st.multiselect("Select preferred travel modes:", mode_options, default=["Flight"])

if st.button("Find Travel Options"):
    if not source or not destination or not mode:
        st.error("⚠️ Please provide all inputs.")
    else:
        input_data = {
            "source": source,
            "destination": destination,
            "mode": ", ".join(mode),
            "format_instructions": format_instructions
        }
        response = chain.invoke(input_data)
        
        if "travel_options" in response:
            st.subheader("🛤️ Available Travel Options:")
            for option in response["travel_options"]:
                st.markdown(f"**Mode:** {option['mode']}")
                st.markdown(f"**Cost:** {option['cost']}")
                st.markdown(f"**Duration:** {option['duration']}")
                st.markdown("---")
        else:
            st.error("⚠️ No travel options found.")
