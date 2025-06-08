import os
import sqlite3
import requests
import spacy
import tkinter as tk
import sys
import spacy

nlp = spacy.load("C:/Python311/Lib/site-packages/en_core_web_sm")

# Ensure compatibility when running as .exe
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# Try loading spaCy model with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Missing spaCy model. Run 'python -m spacy download en_core_web_sm'.")
    sys.exit()  # Corrected 'exit()' issue

# OpenWeather API Key
API_KEY = "9111c7017608b68c2b75feca20318d07"

# Function to fetch weather data
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return f"The temperature in {city} is {data['main']['temp']}°C with {data['weather'][0]['description']}."
    else:
        return "City not found. Try another name!"

# Function to store conversations in SQLite database
def save_conversation(user_input, bot_response):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, user_input TEXT, bot_response TEXT)")
    cursor.execute("INSERT INTO conversations (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()
    conn.close()

# Chatbot response function
def chatbot_nlp_response(user_input):
    doc = nlp(user_input)
    tokens = [token.text.lower() for token in doc]
    
    if "weather" in tokens:
        city = tokens[-1]
        response = get_weather(city)
    elif "name" in tokens:
        response = "I'm your AI chatbot!"
    elif "joke" in tokens:
        response = "Why don't skeletons fight? Because they don't have the guts!"
    else:
        response = "I'm still learning. Ask me differently!"
    
    save_conversation(user_input, response)
    return response

# Function to handle GUI interaction
def send_message(event=None):  # Accept keyboard "Enter" key events
    user_input = user_entry.get().strip()  # Get user input, remove extra spaces

    if user_input:  # Ensure input isn't empty
        bot_response = chatbot_nlp_response(user_input)

        chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        chat_display.insert(tk.END, f"Chatbot: {bot_response}\n\n", "bot")
        chat_display.see(tk.END)  # Auto-scroll to latest message

        user_entry.delete(0, tk.END)  # Clear input field

# GUI Window Setup
app = tk.Tk()
app.title("AI Chatbot")
app.geometry("400x500")

chat_display = tk.Text(app, bg="white", wrap="word", font=("Arial", 12))
chat_display.pack(pady=10)
chat_display.tag_config("user", foreground="blue")
chat_display.tag_config("bot", foreground="green")

user_entry = tk.Entry(app, font=("Arial", 12))
user_entry.pack(pady=5)
user_entry.bind("<Return>", send_message)  # Enable "Enter" key to send messages

send_button = tk.Button(app, text="Send", command=send_message)
send_button.pack()

app.mainloop()