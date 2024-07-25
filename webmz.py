import streamlit as st 
from openai import OpenAI
import requests

api_llm = st.secrets["api_llm"]
api_web = st.secrets["api_web"]
def web(question,api):
     url = "https://serpapi.com/search"
     params = {"q":question, "api_key": api, "engine":"google"}
     response = requests.get(url,params=params)
     response.raise_for_status()
     data = response.json()
     results = data.get("organic_results", [])
     return ' '.join(result.get('snippet', '') for result in results[:5])



def respond(api, prompt):
    client = OpenAI(api_key=api)
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant using web search results to answer questions but you are very creative."},
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content
if "messages" not in st.session_state:
     st.session_state.messages = []
st.title ("السلام عليكم ورحمة الله وبركاته")
st.subheader("انا من اذكى المشاهير")
user = st.text_input("اسألني")
if user:
    result = web(user,api_web)
    if result: 
         prompt = f"Based on these search results, answer the question: '{user}'\n\nResults: {result}"
         ai = respond(api_llm, prompt)
         st.session_state.messages.append({"role":"assistant", "content":ai})
for msg in st.session_state.messages:
     st.write(msg["content"])