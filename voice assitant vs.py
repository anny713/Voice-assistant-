import speech_recognition as sr
import pyttsx3
import requests
import json

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print("User:", query)
        return query
    except Exception as e:
        print("Sorry, I couldn't understand. Can you repeat?")
        return None

def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] == 200:
        weather_desc = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {city} is {weather_desc} with a temperature of {temperature} degrees Celsius."
    else:
        return "Sorry, I couldn't retrieve the weather information."

def main():
    speak("Hello! I am your voice assistant. How can I assist you?")
    while True:
        query = recognize_speech()
        if query:
            if "weather" in query:
                speak("Sure, which city's weather would you like to know?")
                city = recognize_speech()
                if city:
                    weather_info = get_weather(city)
                    speak(weather_info)
            elif "exit" in query or "quit" in query:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I am not programmed to do that yet.")

if __name__ == "__main__":
    main()
