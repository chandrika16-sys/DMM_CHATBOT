import os
import requests
import streamlit as st
from transformers import pipeline

# Real disaster statistics (hypothetical)
statistics = {
    "people_injured": 1200,
    "buildings_damaged": 230,
    "deaths": 43,
    "evacuated": 9500
}

# Emergency contacts (hypothetical)
emergency_contacts = {
    "police": "100",
    "fire department": "101",
    "ambulance": "102",
    "disaster management control room": "1070",
    "electricity department": "1912",
    "local municipality": "1913"
}

# Fetch real-time weather data from API
weather_api_key = '100d1c500f6ed18eb1592b012f49be35'
weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={weather_api_key}&units=metric"
weather_response = requests.get(weather_api_url)

# Initialize the question answering pipeline
qa_pipeline = pipeline("question-answering")

# Placeholder context (to be replaced with actual data)
context = """
The city of Chennai has faced significant challenges in flood management over the years. Despite various efforts, the disaster management strategies have often been criticized for their inefficacy. In particular, the 2015 Chennai floods were devastating, causing widespread damage and loss of life. Issues such as poor urban planning, inadequate drainage systems, and delayed emergency responses have been cited as reasons for the failure in managing the floods effectively.
"""

def generate_answers(questions, context):
    answers = []
    for question in questions:
        try:
            answer = qa_pipeline(question=question, context=context)
            answers.append(answer['answer'])
        except Exception as e:
            answers.append("Error generating answer.")
    return answers

def main():
    st.title("Chennai Floods Disaster Management Chatbot")
    st.header("Chat with the Disaster Management Bot")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("You:", key="input")

    if user_input:
        st.session_state.history.append({"user": user_input})

        if "emergency services" in user_input.lower():
            response = "Here are the emergency contacts:\n"
            for service, contact in emergency_contacts.items():
                response += f"{service}: {contact}\n"
        elif "statistics" in user_input.lower():
            response = f"Disaster Statistics:\nPeople Injured: {statistics['people_injured']}\nBuildings Damaged: {statistics['buildings_damaged']}\nDeaths: {statistics['deaths']}\nEvacuated: {statistics['evacuated']}"
        elif "weather" in user_input.lower():
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                weather = weather_data['weather'][0]['main']
                temp = weather_data['main']['temp']
                response = f"Current weather in Chennai: {temp}°C, {weather}"
            else:
                response = "Failed to fetch weather data. Please try again later."
        else:
            answers = generate_answers([user_input], context)
            response = answers[0] if answers else "No response generated."

        st.session_state.history.append({"bot": response})

    for i, chat in enumerate(st.session_state.history):
        if "user" in chat:
            st.text_area(f"You {i+1}:", value=chat["user"], height=50, max_chars=None, key=f"user_{i}")
        if "bot" in chat:
            st.text_area(f"Bot {i+1}:", value=chat["bot"], height=100, max_chars=None, key=f"bot_{i}")

if __name__ == "__main__":
    main()
