import os
import pyttsx3
import speech_recognition as sr
from AppOpener import open as open_app, close as close_app
import wikipedia
import webbrowser
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak out the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.5  # Set a shorter pause threshold
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language='en-in')
        return query.lower() if query else ""  # Ensure the returned query is lowercased
    except Exception as e:
        return ""  # Return empty string if audio could not be recognized


def main():
    listening = True  # Initially start in listening mode
    while True:
        if listening:
            print("Listening...")  # Print listening mode
            query = take_command()
            if "open " in query:
                app_name = query.replace("open ", "").strip()
                print(f"Opening {app_name}...")
                speak(f"Opening {app_name}")  # Speak out the action
                print("Say 'hey amigo' to resume listening.")
                open_app(app_name, match_closest=True) # Open the app
                listening = False  # Pause listening after performing action
                print("Say 'hey amigo' to resume listening.")
            elif "who is" in query:
                search_terms = query.split("who is", 1)[-1].strip()
                search_terms = " ".join(search_terms.split(" "))
                print(f"Searching Wikipedia for {search_terms}...")
                speak(f"Searching Wikipedia for {search_terms}")  # Speak out the action
                try:
                    page = wikipedia.page(search_terms)
                    print("Opening Wikipedia page...")
                    speak("Opening Wikipedia page")  # Speak out the action
                    webbrowser.open(page.url)
                    print("Say 'hey amigo' to resume listening.")
                except wikipedia.exceptions.PageError:
                    print("No Wikipedia page found.")
                    speak("No Wikipedia page found.")  # Speak out the action
                    print("Say 'hey amigo' to resume listening.")
                except wikipedia.exceptions.WikipediaException as e:
                    print("An error occurred while accessing Wikipedia:", e)
                    speak("An error occurred while accessing Wikipedia.")  # Speak out the action
                    print("Say 'hey amigo' to resume listening.")
                except requests.exceptions.ConnectTimeout:
                    print("Connection to Wikipedia timed out. Please try again later.")
                    speak("Connection to Wikipedia timed out. Please try again later.")  # Speak out the action
                    print("Say 'hey amigo' to resume listening.")
            elif "what is" in query:
                search_term = query.split("what is")[-1].strip()
                print(f"The query is: {search_term}")
                print(f"Searching Chrome for {search_term}...")
                speak(f"Searching Chrome for {search_term}")  # Speak out the action
                search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
                webbrowser.open(search_url)
                print("Say 'hey amigo' to resume.")
            elif "exit" in query:
                print("Quitting...")
                speak("Quitting...")  # Speak out the action
                break  # Exit the loop to stop the entire process
            else:
                listening = False  # Pause listening after unrecognized command
        else:
           # Print recognizing mode
            query = take_command()
            if "hey amigo" in query:
                speak("Listening")  # Speak out the action
                listening = True


if __name__ == '__main__':
    main()

