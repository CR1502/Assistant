import streamlit as st
import pyttsx3
import datetime
import openai
from config import apikey

# Set up OpenAI API
openai.api_key = apikey

# Define global variables
todo_list = []

# Function to add task to to-do list
def add_to_do(task):
    todo_list.append(task)
    say(f"Task '{task}' added to the to-do list.")

# Function to view the to-do list
def view_to_do():
    if not todo_list:
        say("The to-do list is empty.")
    else:
        say("Here are the tasks in your to-do list:")
        for index, task in enumerate(todo_list, 1):
            say(f"{index}. {task}")

# Function to remove task from to-do list
def remove_from_to_do(task_number):
    try:
        task_index = int(task_number) - 1
        removed_task = todo_list.pop(task_index)
        say(f"Task '{removed_task}' removed from the to-do list.")
    except IndexError:
        say("Invalid task number. Please try again.")
    except ValueError:
        say("Invalid input. Please provide a valid task number.")

# Function to clear the to-do list
def clear_to_do():
    todo_list.clear()
    say("To-do list cleared.")

# Function to speak text using pyttsx3
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Main function to run the Streamlit app
def main():
    st.title("Jarvis AI Assistant")

    st.sidebar.header("Options")
    option = st.sidebar.radio("Select an option", ("Add to To-Do List", "View To-Do List", "Remove from To-Do List", "Clear To-Do List"))

    if option == "Add to To-Do List":
        task = st.text_input("Enter task:")
        if st.button("Add Task"):
            add_to_do(task)

    elif option == "View To-Do List":
        view_to_do()

    elif option == "Remove from To-Do List":
        task_number = st.text_input("Enter task number to remove:")
        if st.button("Remove Task"):
            remove_from_to_do(task_number)

    elif option == "Clear To-Do List":
        if st.button("Clear List"):
            clear_to_do()

if __name__ == '__main__':
    main()
