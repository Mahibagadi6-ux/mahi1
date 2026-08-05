import datetime
import os
import subprocess
import webbrowser

import speech_recognition as sr

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class JarvisAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = self._build_voice_engine()
        self.user_name = "Sir"

    def _build_voice_engine(self):
        if pyttsx3 is None:
            return None

        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        return engine

    def speak(self, message):
        print(f"Jarvis: {message}")
        if self.engine is not None:
            self.engine.say(message)
            self.engine.runAndWait()

    def greet(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        self.speak(f"{greeting}, {self.user_name}. Jarvis is online.")

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except OSError:
            return self._type_command("Microphone not found. Type your command")
        except sr.WaitTimeoutError:
            return ""

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You: {command}")
            return command.lower().strip()
        except sr.UnknownValueError:
            self.speak("I did not catch that.")
        except sr.RequestError:
            return self._type_command("Speech service unavailable. Type your command")

        return ""

    def _type_command(self, prompt):
        typed = input(f"{prompt}: ").strip().lower()
        if typed:
            print(f"You: {typed}")
        return typed

    def tell_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The time is {current_time}.")

    def tell_date(self):
        today = datetime.datetime.now().strftime("%d %B %Y")
        self.speak(f"Today's date is {today}.")

    def open_website(self, url, label):
        webbrowser.open(url)
        self.speak(f"Opening {label}.")

    def search_google(self, query):
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.speak(f"Searching Google for {query}.")

    def search_youtube(self, query):
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        self.speak(f"Searching YouTube for {query}.")

    def open_application(self, app_name):
        app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
        }

        executable = app_map.get(app_name)
        if not executable:
            self.speak("I do not know that application yet.")
            return

        try:
            subprocess.Popen(executable)
            self.speak(f"Opening {app_name}.")
        except OSError:
            self.speak(f"I could not open {app_name}.")

    def handle_command(self, command):
        if not command:
            return True

        if any(word in command for word in ["hello", "hi jarvis", "hey jarvis"]):
            self.speak("Hello. What do you need?")
        elif "your name" in command:
            self.speak("I am Jarvis, your Python assistant.")
        elif "time" in command:
            self.tell_time()
        elif "date" in command:
            self.tell_date()
        elif "open google" in command:
            self.open_website("https://www.google.com", "Google")
        elif "open youtube" in command:
            self.open_website("https://www.youtube.com", "YouTube")
        elif "open gmail" in command:
            self.open_website("https://mail.google.com", "Gmail")
        elif command.startswith("search google for "):
            self.search_google(command.replace("search google for ", "", 1))
        elif command.startswith("search youtube for "):
            self.search_youtube(command.replace("search youtube for ", "", 1))
        elif command.startswith("open "):
            app_name = command.replace("open ", "", 1).strip()
            self.open_application(app_name)
        elif "who made you" in command:
            self.speak("I was created with Python.")
        elif "system status" in command:
            self.speak(f"I am running from {os.getcwd()}.")
        elif any(word in command for word in ["stop", "exit", "quit", "shutdown yourself"]):
            self.speak("Shutting down. Goodbye.")
            return False
        else:
            self.speak("Command not recognized. Please try another command.")

        return True


def main():
    assistant = JarvisAssistant()
    assistant.greet()
    assistant.speak(
        "You can ask for time, date, open websites, search Google, search YouTube, or open calculator and notepad."
    )

    running = True
    while running:
        command = assistant.listen()
        running = assistant.handle_command(command)


if __name__ == "__main__":
    main()
