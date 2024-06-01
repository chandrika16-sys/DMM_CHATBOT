import streamlit as st
import requests
import openai
import os

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Real-time weather API endpoint with environment variable
weather_api_key = 100d1c500f6ed18eb1592b012f49be35

weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={weather_api_key}&units=metric"

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
def fetch_weather():
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Houston&appid={weather_api_key}&units=metric")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error fetching weather data: {response.status_code} - {response.json().get('message', '')}")
            return None
    except Exception as e:
        st.error(f"Exception occurred: {e}")
        return None

# Get a response from OpenAI GPT-3
def get_openai_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        message = response.choices[0].text.strip()
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
            weather_data = fetch_weather()
            if weather_data:
                temperature = weather_data["current"]["temp"]
                feels_like = weather_data["current"]["feels_like"]
                pressure = weather_data["current"]["pressure"]
                humidity = weather_data["current"]["humidity"]
                dew_point = weather_data["current"]["dew_point"]
                uvi = weather_data["current"]["uvi"]
                clouds = weather_data["current"]["clouds"]
                visibility = weather_data["current"]["visibility"]
                wind_speed = weather_data["current"]["wind_speed"]
                wind_deg = weather_data["current"]["wind_deg"]
                wind_gust = weather_data["current"]["wind_gust"]

                response = (f"Current weather in Chennai:\n"
                            f"Temperature: {temperature}°C\n"
                            f"Feels Like: {feels_like}°C\n"
                            f"Pressure: {pressure} hPa\n"
                            f"Humidity: {humidity}%\n"
                            f"Dew Point: {dew_point}°C\n"
                            f"UV Index: {uvi}\n"
                            f"Clouds: {clouds}%\n"
                            f"Visibility: {visibility} meters\n"
                            f"Wind Speed: {wind_speed} m/s\n"
                            f"Wind Direction: {wind_deg}°\n"
                            f"Wind Gust: {wind_gust} m/s")
            else:
                response = "Failed to fetch weather data. Please try again later."
        else:
            response = get_openai_response(user_input)
        
        st.session_state.history.append({"bot": response})

    for chat in st.session_state.history:
        if "user" in chat:
            st.text_area("You:", value=chat["user"], height=50, max_chars=None, key=None)
        if "bot" in chat:
            st.text_area("Bot:", value=chat["bot"], height=100, max_chars=None, key=None)

if __name__ == "__main__":
    main()
