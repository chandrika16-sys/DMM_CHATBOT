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

# Resource directories (hypothetical)
resource_directories = {
    "shelters": [
        "Community Hall, Anna Nagar",
        "School Auditorium, T. Nagar",
        "Sports Complex, Velachery"
    ],
    "hospitals": [
        "Apollo Hospital, Greams Road",
        "Fortis Malar Hospital, Adyar",
        "Kauvery Hospital, Alwarpet"
    ],
    "relief_centers": [
        "Relief Center 1, Marina Beach",
        "Relief Center 2, Kotturpuram",
        "Relief Center 3, Mylapore"
    ]
}

# Fetch real-time weather data from API
weather_api_key = '100d1c500f6ed18eb1592b012f49be35'
weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={weather_api_key}&units=metric"
weather_response = requests.get(weather_api_url)

# Initialize the question answering pipeline
qa_pipeline = pipeline("question-answering")

# Realistic and detailed answers
questions = [
    "Why did the disaster management in Chennai fail?",
    "How to improve disaster management in Chennai?",
    "Who are the stakeholders involved in disaster management in Chennai?",
    "How can we as students contribute to disaster management in Chennai?",
    "Is there any need for improvement in disaster management in Chennai?",
    "What role does technology play in disaster management?"
]

answers = [
    "The disaster management in Chennai failed primarily due to a combination of poor urban planning, inadequate drainage systems, and insufficient preparedness. The 2015 Chennai floods were particularly devastating because the city's stormwater drains were not equipped to handle the heavy rainfall. Additionally, there was a lack of coordination among various government agencies, delayed response times, and insufficient early warning systems. Unauthorized construction and encroachments on water bodies also exacerbated the flooding. The city's infrastructure was not resilient enough to withstand such extreme weather events, highlighting the need for better planning and investment in disaster management systems.",
    "Improving disaster management in Chennai requires a multi-pronged approach. Firstly, there needs to be significant investment in upgrading the city's drainage and sewage systems to handle heavy rainfall. Urban planning must prioritize the creation and maintenance of green spaces and water bodies to absorb excess rainwater. The government should implement strict regulations to prevent unauthorized construction and encroachments on natural waterways. Additionally, there should be a focus on developing robust early warning systems and conducting regular disaster preparedness drills. Community awareness programs are essential to educate residents on how to respond during emergencies. Collaboration between government agencies, NGOs, and local communities is crucial to create an effective disaster management framework.",
    "The stakeholders involved in disaster management in Chennai include various government agencies such as the Chennai Corporation, Tamil Nadu State Disaster Management Authority (TNSDMA), and the Public Works Department (PWD). Other key stakeholders are emergency services like the police, fire department, and ambulance services. Non-governmental organizations (NGOs) and community groups play a vital role in providing relief and rehabilitation during disasters. The Meteorological Department is responsible for providing weather forecasts and early warnings. Additionally, residents and local businesses are also important stakeholders, as their preparedness and response can significantly impact the effectiveness of disaster management efforts.",
    "Students can play a crucial role in disaster management in Chennai by participating in awareness campaigns and preparedness programs. They can volunteer with NGOs and community organizations to assist in relief and rehabilitation efforts during disasters. Students can also use social media and other platforms to spread information about safety measures and emergency contacts. Additionally, they can participate in or organize community drills and training sessions to educate others on how to respond during emergencies. By being proactive and engaged, students can contribute to building a more resilient community.",
    "There is an ongoing need for improvement in disaster management in Chennai. While some measures have been implemented since the 2015 floods, challenges remain. Continuous investment in infrastructure, such as upgrading drainage systems and creating flood-resistant buildings, is essential. The government should enhance early warning systems and ensure timely dissemination of information to the public. Regular training and capacity-building programs for emergency responders are necessary to improve response times and coordination. Public awareness campaigns should be conducted to educate residents about disaster preparedness and response. Additionally, it is crucial to involve local communities in planning and decision-making processes to ensure that disaster management strategies are effective and inclusive.",
    "Technology plays a crucial role in modern disaster management, significantly enhancing the ability to prepare for, respond to, and recover from disasters. In the context of Chennai floods, the following technologies are particularly important:\n\n"
    "1. **Early Warning Systems**: Advanced meteorological tools and satellite imagery can predict heavy rainfall and potential flooding. These systems provide early warnings to residents and authorities, allowing for timely evacuation and preparation.\n\n"
    "2. **Geographic Information Systems (GIS)**: GIS technology helps in mapping flood-prone areas, planning evacuation routes, and coordinating relief efforts. Real-time data from GIS can be used to monitor flood levels and affected areas.\n\n"
    "3. **Drones**: Drones are used for aerial surveys and real-time monitoring of affected areas. They provide critical information about the extent of flooding and damage, helping in efficient allocation of resources and aid.\n\n"
    "4. **Mobile Technology and Social Media**: Mobile apps and social media platforms are essential for disseminating information quickly to the public. They help in spreading awareness, providing updates, and coordinating rescue operations.\n\n"
    "5. **Artificial Intelligence (AI) and Machine Learning (ML)**: AI and ML can analyze large datasets to predict disaster patterns, optimize response strategies, and improve decision-making. These technologies help in identifying vulnerable areas and populations, ensuring better preparedness.\n\n"
    "6. **Internet of Things (IoT)**: IoT devices, such as sensors and smart meters, can monitor water levels, weather conditions, and infrastructure status in real-time. This data is crucial for early detection of potential hazards and proactive response.\n\n"
    "7. **Resilient Infrastructure**: Modern construction technologies and materials can create flood-resistant buildings and infrastructure, reducing the impact of disasters.\n\n"
    "By leveraging these technologies, Chennai can enhance its disaster management capabilities, ensuring better protection for its residents and faster recovery from future floods."
]

def generate_answer(question, context):
    try:
        answer = qa_pipeline(question=question, context=context)
        return answer['answer']
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return "Sorry, I couldn't generate an answer at the moment."

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
            response = f"Disaster Statistics:\nPeople Injured: {statistics['people_injured']}\n Buildings Damaged: {statistics['buildings_damaged']}\n Deaths: {statistics['deaths']}\n Evacuated: {statistics['evacuated']}"
        elif "weather" in user_input.lower():
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                weather = weather_data['weather'][0]['main']
                temp = weather_data['main']['temp']
                response = f"Current weather in Chennai: {temp}°C, {weather}"
            else:
                response = "Failed to fetch weather data. Please try again later."
        elif "shelters" in user_input.lower():
            response = "Here are the locations of available shelters:\n"
            for shelter in resource_directories["shelters"]:
                response += f"- {shelter}\n"
        elif "hospitals" in user_input.lower():
            response = "Here are the locations of nearby hospitals:\n"
            for hospital in resource_directories["hospitals"]:
                response += f"- {hospital}\n"
        elif "relief centers" in user_input.lower():
            response = "Here are the locations of relief centers:\n"
            for center in resource_directories["relief_centers"]:
                response += f"- {center}\n"
        elif "resource help" in user_input.lower():
            response = "For resource help, please specify if you need shelters, hospitals, or relief centers."
        else:
            # Default to answering predefined questions
            question_index = -1
            for i, q in enumerate(questions):
                if q.lower() in user_input.lower():
                    question_index = i
                    break

            if question_index != -1:
                context = " ".join(answers)
                response = generate_answer(questions[question_index], context)
            else:
                response = "I'm sorry, I didn't understand your question. Please ask about emergency services, statistics, weather, shelters, hospitals, or relief centers."

        st.session_state.history[-1]["bot"] = response

    for chat in st.session_state.history:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")

if __name__ == "__main__":
    main()
