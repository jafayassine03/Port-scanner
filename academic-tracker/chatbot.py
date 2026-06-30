import json
import os
import random
import threading
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

FILE = "chat_history.json"


class ChatBot:
    def __init__(self):
        self.name = None
        self.mood = "neutral"
        self.history = self.load_history()  # ✅ LOAD EXISTING HISTORY

        self.greetings = ["Hello!", "Hey there!", "Hii", "What's up!"]
        self.how_are_you_responses = [
            "I'm doing great ",
            "Feeling awesome today!",
            "All good here!",
        ]

        self.quotes = [
            "Believe you can and you're halfway there.",
            "Keep going, you’re doing amazing!",
            "Happiness depends upon ourselves.",
            "Do one thing every day that scares you.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts."
        ]

        self.weather_conditions = [
            "Sunny ☀️",
            "Cloudy ☁️",
            "Rainy 🌧️",
            "Stormy ⛈️",
            "Windy 🌬️",
            "Snowy ❄️"
        ]

    # ---------- HISTORY SYSTEM ----------
    def load_history(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(FILE, "w") as f:
            json.dump(self.history, f, indent=4)

    def clear_history(self):
        self.history = []
        self.save_history()
        return "History cleared 🧹"

    # ---------- EXISTING FEATURES ----------
    def banner(self):
        print(Fore.YELLOW + "Simple Smart ChatBot")
        print(Fore.YELLOW + "Type 'help' for commands.\n")

    def get_time(self):
        return datetime.now().strftime("Current time: %H:%M")

    def get_date(self):
        return datetime.now().strftime("Today's date: %Y-%m-%d")

    def tell_joke(self):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs 🐛",
            "Why did Python go to therapy? Too many issues.",
            "I would tell you a UDP joke… but you might not get it."
        ]
        return random.choice(jokes)

    def tell_quote(self):
        return random.choice(self.quotes)

    def get_weather(self):
        condition = random.choice(self.weather_conditions)
        temp = random.randint(15, 35)
        return f"Today's weather looks {condition} with around {temp}°C."

    def detect_mood(self, text):
        if any(word in text for word in ["sad", "upset", "tired"]):
            self.mood = "sad"
            return "I'm here for you. Want to talk about it?"
        if any(word in text for word in ["happy", "great", "good"]):
            self.mood = "happy"
            return "I love that energy 😄"
        return None

    def calculate(self, expression):
        try:
            result = eval(expression)
            return f"Result: {result}"
        except:
            return "Invalid calculation ❌"

    def show_history(self):
        if not self.history:
            return "No history yet."
        return "\n".join(self.history[-10:])

    def help_menu(self):
        return (
            "Commands:\n"
            "- hi / hello\n"
            "- my name is <name>\n"
            "- how are you\n"
            "- time\n"
            "- date\n"
            "- joke\n"
            "- quote\n"
            "- weather\n"
            "- calculate <math>\n"
            "- remind me to <task> in <seconds/minutes>\n"
            "- history\n"
            "- save\n"
            "- clear history\n"
            "- exit"
        )

    # ---------- REMINDER ----------
    def set_reminder(self, text):
        try:
            parts = text.split("in")
            message = parts[0].replace("remind me to", "").strip()
            time_part = parts[1].strip()

            if "second" in time_part:
                seconds = int(time_part.split()[0])
            elif "minute" in time_part:
                seconds = int(time_part.split()[0]) * 60
            else:
                return "Invalid time format."

            threading.Thread(target=self.reminder_thread, args=(message, seconds)).start()

            return f"I will remind you to '{message}' in {time_part} ⏰"

        except:
            return "Couldn't set reminder."

    def reminder_thread(self, message, seconds):
        time.sleep(seconds)
        print(Fore.GREEN + f"\n⏰ Reminder: {message}\n")

    # ---------- MAIN LOOP ----------
    def run(self):
        self.banner()

        while True:
            user_input = input(Fore.CYAN + "You: " + Style.RESET_ALL).strip().lower()

            self.history.append(f"You: {user_input}")

            if user_input in ["exit", "quit", "bye"]:
                self.save_history()
                print(Fore.MAGENTA + "Bot: Goodbye 👋 (history saved)")
                break

            if user_input == "save":
                self.save_history()
                print(Fore.MAGENTA + "Bot: History saved 💾")
                continue

            if user_input == "clear history":
                response = self.clear_history()
                print(Fore.MAGENTA + f"Bot: {response}")
                continue

            if user_input in ["hi", "hello", "hey"]:
                response = random.choice(self.greetings)
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input.startswith("my name is"):
                self.name = user_input.replace("my name is", "").strip().title()
                response = f"Nice to meet you, {self.name}!"
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if "how are you" in user_input:
                response = random.choice(self.how_are_you_responses)
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "time":
                response = self.get_time()
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "date":
                response = self.get_date()
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "joke":
                response = self.tell_joke()
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "quote":
                response = self.tell_quote()
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "weather":
                response = self.get_weather()
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input.startswith("calculate"):
                expression = user_input.replace("calculate", "").strip()
                response = self.calculate(expression)
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input.startswith("remind me to"):
                response = self.set_reminder(user_input)
                print(Fore.MAGENTA + f"Bot: {response}")
                self.history.append(f"Bot: {response}")
                continue

            if user_input == "history":
                response = self.show_history()
                print(Fore.MAGENTA + f"Bot:\n{response}")
                continue

            if user_input == "help":
                response = self.help_menu()
                print(Fore.MAGENTA + f"Bot: {response}")
                continue

            mood_response = self.detect_mood(user_input)
            if mood_response:
                print(Fore.MAGENTA + f"Bot: {mood_response}")
                self.history.append(f"Bot: {mood_response}")
                continue

            response = "Hmm… I’m still learning 🤔"
            print(Fore.MAGENTA + f"Bot: {response}")
            self.history.append(f"Bot: {response}")