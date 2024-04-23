import openai
import speech_recognition as sr
import os
import webbrowser
import datetime
import pyttsx3
from config import apikey
import requests

openai.api_key = apikey
chatStr = ""
todo_list = []
is_standby = False

def add_to_do(task):
    todo_list.append(task)
    say(f"Task '{task}' added to the to-do list.")

def view_to_do():
    if not todo_list:
        say("The to-do list is empty.")
    else:
        say("Here are the tasks in your to-do list:")
        for index, task in enumerate(todo_list, 1):
            say(f"{index}. {task}")

def remove_from_to_do(task_number):
    try:
        task_index = int(task_number) - 1
        removed_task = todo_list.pop(task_index)
        say(f"Task '{removed_task}' removed from the to-do list.")
    except IndexError:
        say("Invalid task number. Please try again.")
    except ValueError:
        say("Invalid input. Please provide a valid task number.")

def clear_to_do():
    todo_list.clear()
    say("To-do list cleared.")

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry"

def get_weather(location):
    say("Please say the location for weather information.")
    query = takecommand().lower()
    location = query.split("in")[-1].strip()

    if not location:
        say("Could not identify the location. Please try again.")
        return

    search_query = f"weather in {location} site:weather.com"
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(url)

def get_news():
    say("Opening Google News...")
    url = "https://news.google.com/"
    webbrowser.open(url)

def play_music():
    say("Sure, which song or artist would you like to listen to?")
    query = takecommand().lower()
    search_query = f"https://music.youtube.com/search?q={query}"
    webbrowser.open(search_query)

def get_system_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."

def write_email():
    say("What should the email be about?")
    email_topic = takecommand()

    email_content = f"Email about {email_topic}."
    response = openai.Completion.create(
        engine="davinci-002",
        prompt=email_content,
        max_tokens=100,
    )
    email_variation = response.choices[0].text.strip()
    say(email_variation)

    say("Would you like to save this email as a text file on the desktop?")
    save_email = takecommand().lower()
    if "yes" in save_email:
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        with open(f"{desktop_path}/email.txt", "w") as f:
            f.write(email_variation)
        say("Email saved on the desktop as email.txt.")
    else:
        say("Email not saved.")

def google_search(query):
    search_query = query.replace("search", "").strip()
    say(f"What should I search for related to {search_query}?")
    search_query = takecommand()
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(url)

def chat_with_user():
    questions = [
        "What's your name?",
        "Where are you from?",
        "What do you do for a living?",
        "Do you have any hobbies?",
    ]
    for question in questions:
        say(question)
        answer = takecommand()
        say(f"You said {answer}")

if __name__ == '__main__':
    print("Say something")
    say("Hello Sir I am Jarvis. How can I help you?")

    while True:
        print("Listening...")
        query = takecommand()

        if "add to my list" in query.lower():
            task = query.split("add to my list")[-1].strip()
            add_to_do(task)

        elif "view my list" in query.lower():
            view_to_do()

        elif "remove from my list" in query.lower():
            task_number = query.split("remove from my list")[-1].strip()
            remove_from_to_do(task_number)

        elif "clear my list" in query.lower():
            clear_to_do()

        elif "weather" in query.lower():
            location = query.split("in")[-1].strip()
            weather_info = get_weather(location)
            say(weather_info)

        elif "latest news" in query.lower():
            get_news()

        elif "music" in query:
            play_music()

        elif "time" in query.lower():
            time_info = get_system_time()
            say(time_info)

        elif "email" in query.lower():
            write_email()

        elif "search" in query.lower():
            google_search(query)

        elif "chat" in query.lower():
            chat_with_user()

        elif "quit" in query.lower():
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("No specific command found, chatting with user")
            chat_with_user()
