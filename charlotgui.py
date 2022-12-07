import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import threading as tr
from tkinter import *
from PIL import Image, ImageTk
import os
from pygame import mixer

main_window= Tk()
main_window.title("Charlot IA")
main_window.geometry("900x500")
main_window.resizable(0,0)
main_window.configure(bg='#283048')

label_title= Label(main_window, text="Charlot IA",bg="#859398",fg="#EAEAEA",font=("Arial", 30, "bold"))
label_title.pack(pady=10)

charlot_foto= ImageTk.PhotoImage(Image.open("Mi proyecto.jpg"))
windows_foto= Label(main_window, image=charlot_foto)
windows_foto.pack(pady=5)

def mexican_voice():
    change_voice(0)
def english_voice():
    change_voice(1)
def spanish_voice():
    change_voice(2)
def change_voice(id):
    engine.setProperty('voices', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy Charlot en que te puedo ayudar?")

name = "Charlot"
listerner = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
engine.setProperty('rate', 145)

sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'twitch': 'twitch.tv',
    'facebook': 'facebook.com',
    'tioanime': 'tioanime.com',
    'cursos': 'freecodecamp.org/espanol/learn'
}

programs = {
    'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
    'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
    'League of legends': r"C:\Riot Games\League of Legends\LeagueClient.exe",
    'EVE Online': r'C:\EVE\Launcher\evelauncher.exe',
    'Albion Online': r'C:\Program Files (x86)\AlbionOnline\launcher\AlbionLauncher.exe'
}


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Te estoy escuchando...")
            listener.adjust_for_ambient_noise(source)
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec


def clock(rec):
    num  = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las  "+ num +"horas")
    if num [0] =='0'and len (num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime("%H:%M") == num:
            print("DESPIERTA!!!!")
            mixer.init()
            mixer.music.load("auronplay_alarma.mp3")
            mixer.music.play()
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

def iniciar_charlot():
    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ":" + wiki)
            talk(wiki)
        elif 'alarm' in rec:
            t = tr.Thread(target=clock, args=(rec,))
            t.start()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe{sites[site]}', shell=True)
                    talk(f'abriendo{sites}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo{app}')
                    os.startfile(programs[app])
        elif 'escribe' in rec:
            try:
                with open('nota.txt', 'a')as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk("Adiós!")
            break


def write(f):
    talk("Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("Nota.txt", shell=True)

button_voicemx= Button(main_window,text="Voz México",fg="white",bg="#45B649",font=("Arial",22,"bold"),command=mexican_voice)
button_voicemx.place(x=700,y=75,width=180,height=65)
button_voicemx= Button(main_window,text="Voz España",fg="white",bg="#c31432",font=("Arial",22,"bold"),command=spanish_voice)
button_voicemx.place(x=700,y=145,width=180,height=65)
button_voicemx= Button(main_window,text="Voz ingles",fg="white",bg="#4286f4",font=("Arial",22,"bold"),command=english_voice)
button_voicemx.place(x=700,y=215,width=180,height=65)


main_window.mainloop()