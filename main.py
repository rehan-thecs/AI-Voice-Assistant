import speech_recognition as sr
import pyttsx3
import openai
import os
import sys
import threading
import time
import pyaudio

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Speech Recognition request failed: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error in listen function: {e}")
            return ""

def chat_with_gpt(prompt):
    try:
        client = openai.OpenAI(api_key="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")  # Use api
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            # model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat_with_gpt function: {e}")
        return "I'm sorry, but I encountered an error processing your request."

def assistant_loop():
    while True:
        try:
            query = listen()
            if query:
                if "exit" in query or "shutdown" in query:
                    speak("Goodbye!")
                    sys.exit()
                response = chat_with_gpt(query)
                speak(response)
        except Exception as e:
            print(f"Error in assistant_loop: {e}")
        time.sleep(1)  # Small delay to prevent rapid looping

def run_on_startup():
    try:
        if sys.platform == "win32":
            startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            script_path = os.path.abspath(__file__)
            shortcut_path = os.path.join(startup_path, "assistant.lnk")
            with open(shortcut_path, "w") as shortcut:
                shortcut.write(f"@echo off\npython {script_path}")
        elif sys.platform == "linux":
            os.system(f"echo 'python3 {os.path.abspath(__file__)} &' >> ~/.bashrc")
    except Exception as e:
        print(f"Error in run_on_startup function: {e}")

if __name__ == "__main__":
    run_on_startup()
    threading.Thread(target=assistant_loop).start()
