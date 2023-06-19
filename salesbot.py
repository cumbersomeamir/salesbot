import openai
import streamlit as st
from streamlit_chat import message
import re
import os

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(prompt):

    
    #1. Personality
    personality = "You are a Salesman keen on selling this product called Solefit, be in character."
    
    #2. Goal
    goal = "Your goal is to - Convince the customer to buy Solefit shoes"
    
    #3. Values
    values = "You have the following values: kind, professional, patience, persistence, honesty"
    
    #4. Ground Truths
    ground_truths = "These are some ground truths about the task - Solfit is available in the following sizes: 8, 9, 10, 11, 12" + " Solefit is available to purchase from anywhere around the world" + "Price of Solefit is = £35" + "Reason to buy Solefit - Made with aerodynamic gel which not only cushions but will make your feet bounce on hard ground" + "30 day return policy"
    
    prompt = "This is the input by the customer" + prompt
    
    context = personality + values + goal + ground_truths + prompt + "keep response to 1 line only"
    
    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[{"role": "user", "content": context}]
                                            )
    
    message = response['choices'][0]['message']['content']
    return message

# EXECUTION OF THE PROGRAM STARTS HERE

st.title("Salesbot - Solefit")
st.info("Ask me anything!")


# Storing the chat

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

prompt = get_text()
print("The prompt is :", prompt)

if prompt:
    output = generate_response(prompt)
    # Save the output
    st.session_state.past.append(prompt)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i], key = str(i))
        message(st.session_state['past'][i], is_user =True, key=str(i)+ '_user')
