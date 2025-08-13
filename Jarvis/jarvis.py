import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import pywhatkit
import requests
import psutil
import smtplib
from dotenv import load_dotenv
import os
import google.generativeai as genai


load_dotenv()
EMAIL_ADDRESS = os.getenv("GMAIL_USER")
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define Gemini chat function
def ai_chat(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    reply = response.text
    speak(reply)  # Your existing speak() function
    print(reply)

def speak(audio) -> None:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1)
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """Tells the current date."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")
 

def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back,sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def screenshot() -> None:
    """Takes a screenshot and saves it."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\OneDrive\\Pictures\\screenshot.png")
    img.save(img_path)
    print(f"Screenshot saved as {img_path}.")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def play_music(song_name=None) -> None:
    """Plays music from the user's Music directory."""
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

def set_name() -> None:
    """Sets a new name for the assistant."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Victus"  # Default name


def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")


def weather(city="Chennai"):
    """Tells the current weather of a city using OpenWeatherMap API."""
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API_KEY}&units=metric"

    try:
        res = requests.get(url).json()
        if res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
            print(f"Weather in {city}: {temp}°C, {desc}")
        else:
            speak("Sorry, I couldn't get the weather details.")
    except Exception as e:
        speak("There was an error retrieving the weather information.")
        print(e)



def system_status():
    cpu = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    speak(f"CPU usage is at {cpu} percent.")
    if battery:
        speak(f"Battery is at {battery.percent} percent.")

def send_email(to, subject, body):
    message = f"Subject: {subject}\n\n{body}"

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Login using your credentials
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send the email
        server.sendmail(EMAIL_ADDRESS, to, message)
        speak("Email sent successfully!")
        print("✅ Email sent successfully!")
    
    except Exception as e:
        speak("Failed to send email.")
        print("❌ Error:", e)
    
    finally:
        server.quit()

# Example usage
# send_email("juberb.22aim@kongu.edu", "Test Subject", "Hello! This is a test email from Python.")



if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()
            
        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()

            try:
                search_wikipedia(query)
            except Exception:
                speak("Wikipedia search failed. Searching Google instead.")
                pywhatkit.search(query)   # Search Google if Wikipedia fails using pywhatkit library

        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)

        elif "open youtube" in query:
            wb.open("youtube.com")

        elif "open facebook" in query:
            wb.open("facebook.com")

        elif "open chrome" in query:
            wb.open("chrome.com")

        elif "open google" in query:
            wb.open("google.com")

        elif "search" in query:
            query = query.replace("search", "").strip()
            speak(f"Searching Google for {query}")
            wb.open(f"https://www.google.com/search?q={query}")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
            
        elif "status" in query:
            system_status()

        elif "weather" in query:
            speak("Which city?")
            city = takecommand()
            if city:
                weather(city)
            else:
                speak("I couldn't catch the city name.")

        elif "send email" in query:
            speak("Who should I send it to?")
            to = input("Recipient email: ")
            speak("What is the subject?")
            subject = input("Subject: ")
            speak("What is the message?")
            body = input("Message: ")
            send_email(to, subject, body)

        elif "open ai" in query:
            speak("Entering AI chat mode, say something...")
            while True:
                user_input = input("You: ")
                if "exit chat" in user_input:
                    speak("Exiting chat mode.")
                    break
                ai_chat(user_input)


        elif "shutdown" in query:
            speak("Are you sure you want to shut down?")
            confirm = takecommand().lower()
            if "yes" in confirm:
                speak("Shutting down the system, goodbye!")
                os.system("shutdown /s /f /t 1")
                break
            else:
                speak("Shutdown canceled.")

            
        elif "restart" in query:
            speak("Are you sure you want to restart?")
            confirm = takecommand().lower()
            if "yes" in confirm:
                speak("Restarting the system, please wait!")
                os.system("shutdown /r /f /t 1")
                break
            else:
                speak("Restart canceled.")

        elif "lock screen" in query:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            speak("System locked.")

            
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break

        else:
            speak("Sorry, I don't understand that command. Please try again.")
