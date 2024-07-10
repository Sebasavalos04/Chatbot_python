import json
import random
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

engine = pyttsx3.init()

#Configuramos la voz del bot
def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate',140)
    engine.say(text)
    engine.runAndWait()

#Reconoce la voz y la convierte a texto
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Por favor, hable ahora...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='es')
            return text
        except:
            return ""

#Carga el archivo json
def load_intents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        intents = json.load(file)
    return intents

#Genera respuestas a traves de los intents
def get_response(intents, user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input.lower():
                return random.choice(intent['responses'])
    return "No estoy seguro de cómo responder a eso."


def main():
    user_input = recognize_speech()
    if user_input.lower() in ["salir", "terminar", "adiós"]:
        speak("No dudes en hablarme cuando lo necesites!")
        root.quit()
    if user_input:
        response = get_response(intents, user_input)
        chat_log.config(state='normal')
        chat_log.insert(tk.END, "Tú: " + user_input + "\n", 'user')
        chat_log.insert(tk.END, "Bot: " + response + "\n\n", 'bot')
        chat_log.config(state='disabled')
        chat_log.yview(tk.END)
        speak(response)
    status_label.config(text="Listo para escuchar", foreground="black")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Chatbot de Voz")
root.geometry("600x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TFrame", background="#f0f0f0")

main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

chat_log = scrolledtext.ScrolledText(main_frame, state='disabled', wrap='word', width=70, height=20, font=("Helvetica", 10))
chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

chat_log.tag_config('user', foreground='blue')
chat_log.tag_config('bot', foreground='green')

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=1, column=0, pady=10)

talk_button = ttk.Button(button_frame, text="Hablar", command=main)
talk_button.grid(row=0, column=0, padx=5)

quit_button = ttk.Button(button_frame, text="Salir", command=root.quit)
quit_button.grid(row=0, column=1, padx=5)

status_label = ttk.Label(main_frame, text="Listo para escuchar", font=("Helvetica", 10))
status_label.grid(row=2, column=0, columnspan=2, pady=10)

# Carga de los intents
intents = load_intents('intents.json')

# Inicia la interfaz gráfica
root.mainloop()