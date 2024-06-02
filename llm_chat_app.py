import os
import requests
import streamlit as st

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

# Function to get a response from OpenAI GPT
def get_openai_response(prompt):
    try:
        response = requests.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
            },
            json={
                "prompt": prompt,
                "max_tokens": 150
            }
        )
        data = response.json()
        message = data['choices'][0]['text'].strip()
        return message
    except Exception as e:
        st.error(f"Error fetching response from OpenAI: {e}")
        return "Sorry, I couldn't process your request at the moment."

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
            prompt = f"Question: {user_input}\nContext: The city of Chennai has faced significant challenges in flood management over the years. Despite various efforts, the disaster management strategies have often been criticized for their inefficacy. In particular, the 2015 Chennai floods were devastating, causing widespread damage and loss of life. Issues such as poor urban planning, inadequate drainage systems, and delayed emergency responses have been cited as reasons for the failure in managing the floods effectively.\nAnswer:"
            response = get_openai_response(prompt)

        st.session_state.history.append({"bot": response})

    for i, chat in enumerate(st.session_state.history):
        if "user" in chat:
            st.text_area(f"You {i+1}:", value=chat["user"], height=50, max_chars=None, key=f"user_{i}")
        if "bot" in chat:
            st.text_area(f"Bot {i+1}:", value=chat["bot"], height=100, max_chars=None, key=f"bot_{i}")

if __name__ == "__main__":
    main()
