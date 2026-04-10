import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

#load secret from env file
load_dotenv()
API_KEY=os.getenv("GEMINI_API_KEY")

# Safety check: Stop if the key is missing
if not API_KEY:
    st.error("Missing API Key! Please check your .env file.")
    st.stop()

#Page Title
st.title("NB AI App 🤖")

#Configure the AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite') #Fast free small model. Latest free version with data until 2017

#Create a Memory Bank
#Step1: create an empty_list
if 'my_chat_history' not in st.session_state:
    st.session_state.my_chat_history=[]
#Step2: Show old messages first
#When page returns it should show old chat history
for chat in st.session_state.my_chat_history:
    st.write(f"**{chat['role']}**: {chat['text']}")

#What we see
st.write("Welcome! Ask me anything")
# 3. Input Area
user_input = st.text_input("Enter your prompt:", placeholder="Type here...")

#create a button to submit
if st.button("Send to AI"):
    if user_input:
        #4.Save your question to memory FIRST
        st.session_state.my_chat_history.append({"role": "You", "text": user_input})
        with st.spinner("Thinking..."):
            #send the text to AI and get response
            response = model.generate_content(user_input)
            
            #5.Save AI response to memory SECOND
            st.session_state.my_chat_history.append({"role": "AI", "text": response.text})    
        
            #6.Rerun the app to show the new messages immediately
            st.rerun()
    else:
        st.warning("Please type something first!")
