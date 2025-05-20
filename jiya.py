import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import smtplib
import pyaudio
import wikipedia
import tasks
import noisereduce as nr
import io
import requests
import soundfile as sf



# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# DeepSeek API Key (Replace with your actual key)
DEEPSEEK_API_KEY = "sk-6d27660144e147b1b9978c48263e98a2"  # Step 1 from search result 2.

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello sir, I'm your personal assistant.")

def search_wikipedia(query):
    try:
        # Set the language for Wikipedia
        wikipedia.set_lang("en")

        # Fetch the summary of the query from Wikipedia
        summary = wikipedia.summary(query, sentences=2)  # Get a brief summary
        speak(summary)

    except Exception as e:
        speak("Sorry, I couldn't find any information on that topic.")

def take_command():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        # print(e)    
        print("i did not here that please say it again...")
        speak("i did not here that please say it again...")#Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query.lower()


def open_website(url):
    webbrowser.open(url)

def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')  # Use your email and password
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def get_current_time():
    n = datetime.datetime.now()
    current_time = n.strftime("%H:%M:%S")
    speak("It's ")
    speak(current_time)

    hour = int(n.hour) #Correctly get hour
    if hour < 12:
        speak("And Morning!, what you like to do sir....")
    elif 12 <= hour < 18:
        speak("And Afternoon!, what you like to do sir....")
    else:
        speak("And Evening!, what you like to do sir....")

def add_date():
    speak("In Which Date you want for task....")
    date = take_command()
    return date

def add_month():
    speak("In Which Month you want for task....")
    month = take_command()
    return month

def add_year():
    speak("In Which Year you want for task....")
    year = take_command()
    return year

def add_task():
    speak("Yes sir, which tasks you want to add....")
    task = take_command()
    return task

def p_d_tasks(a_date):
    # You'll need to flesh out this function to actually retrieve tasks
    # based on the date. For now, it just returns True.
    return True  # Placeholder

def deepseek_search(query):
    """
    Searches DeepSeek and returns the first 5 lines of the response.
    """
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",  # Or "deepseek-reasoner"
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']

        lines = content.splitlines()
        first_5_lines = "\n".join(lines[:5])
        return first_5_lines

    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API: {e}")
        return "Sorry, I encountered an error while searching DeepSeek."
    except (KeyError, IndexError) as e:
        print(f"Error parsing DeepSeek response: {e}")
        return "Sorry, I couldn't parse the information from DeepSeek."

if __name__ == "__main__":
    wish_me()
    task = tasks.remember()  # Assuming tasks.remember() exists and works
    speak("Today's Tasks are:")
    speak(task)

    while True:
        command = take_command()

        if not command:  # If take_command() returned an empty string due to error
            continue # skip rest of loop and retry take_command

        if 'open youtube' in command:
            open_website("https://www.youtube.com")

        elif 'open google' in command:
            open_website("https://www.google.com")

        elif 'send email' in command:
            try:
                speak("What should I say?")
                content = take_command()
                to = "recipient_email@gmail.com"  # Change to recipient's email
                send_email(to, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry, I could not send the email.")

        elif 'wikipedia' in command:
            search_wikipedia(command)

        elif 'what time' in command:
            get_current_time()

        elif 'find tasks' in command:
            date = add_date()
            month = add_month()
            year = add_year()
            a_date = "-".join([year, month, date])
            bol = p_d_tasks(a_date)
            speak(bol)

        elif 'add task' in command:
            date = add_date()
            month = add_month()
            year = add_year()
            task_description = add_task()
            a_date = "-".join([year, month, date])
            bol = tasks.addtask(a_date, task_description) #fixed typo a_taks
            speak(bol)

        elif 'ai' in command:
            query = command.replace('search deepseek', '').strip()
            results = deepseek_search(query)
            speak("Here's what I found on DeepSeek:")
            speak(results)

        elif 'quit' in command:
            speak("Goodbye!")
            break
