import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
import app
from threading import Thread
import json
import requests
from bs4 import BeautifulSoup


today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


file_exp_status = False
files =[]
path = ''
is_awake = True  


def reply(audio):
    app.ChatBot.addAppMsg(audio)

    print(audio)
    engine.say(audio)
    engine.runAndWait()




def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("Hello Boss , At your service ?")


with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False


def record_audio():
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        voice_data = ''
        audio = r.listen(source, phrase_time_limit=5)

        try:
            voice_data = r.recognize_google(audio)
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            print('cant recognize')
            pass
        return voice_data.lower()

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def respond(voice_data):
    global file_exp_status, files, is_awake, path
    print(voice_data)
    voice_data.replace('jarvis','')
    app.eel.addUserMsg(voice_data)

    if is_awake==False:
        if 'wake up' in voice_data:
            is_awake = True
            wish()

    
    elif 'hello' in voice_data:
        wish()

    elif 'send email' in voice_data:    
        reply("What should I say?")
        message = record_audio()
        app.eel.addUserMsg(message)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("your-email", "your-password")
        reply('Whom should I send this email?')
        to = record_audio().lower()
        app.eel.addUserMsg(to)
        s.sendmail("your-email", to, message)  
        s.quit()
        reply("Email has been sent!")

    elif 'shutdown' in voice_data:
        reply("Do you want to shut down your computer?")
        confirm = record_audio()
        app.eel.addUserMsg(confirm)
        if "yes" in confirm or "yeah" in confirm:
            os.system("shutdown /s /t 1")
        else:
            reply("Operation aborted.")  
    elif 'restart' in voice_data:
        reply("Do you want to restart your computer?")
        confirm = record_audio()
        app.eel.addUserMsg(confirm)
        if "yes" in confirm or "yeah" in confirm:
            os.system("shutdown /r /t 1")
        else:
            reply("Operation aborted.")  
    elif 'logout' in voice_data:
        reply("Do you want to log out of your computer?")
        confirm = record_audio()
        app.eel.addUserMsg(confirm)
        if "yes" in confirm or "yeah" in confirm:
            os.system("shutdown -l")
        else:
            reply("Operation aborted.")   

    elif "daily news" in voice_data:
        reply("Here are the top headlines for today:")
        # url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=<c04544ddb4324fecb79d6660cd0d616a>"
        # response = requests.get(url)
        # news = json.loads(response.text)
        # for article in news['articles']:
        #     reply(article['title'])   
        url = 'https://www.bbc.com/news'
        response = requests.get(url)   
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find('body').find_all('h3')
        for x in headlines:
            reply(x.text.strip())

    elif 'volume up' in voice_data:
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        reply("Volume increased.")


    elif 'volume down' in voice_data:
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        reply("Volume decreased.")


    elif 'take screenshot' in voice_data:
        screenshot = pyautogui.screenshot()
        screenshot.save('screenshot.png')
        reply("Screenshot taken!")


    elif 'record video' in voice_data:
        reply("Starting video recording...")
        os.system("start microsoft.windows.camera:")


    elif 'open calculator' in voice_data:
        os.system('start calc.exe')
        reply("Calculator has been opened.")
        
    elif 'where is' in voice_data:
        data = voice_data.split(" ")
        location = data[2]
        reply("Hold on Sir, I will show you where " + location + " is.")
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")    


    elif 'open notepad' in voice_data:
        os.system('start notepad.exe')
        reply("Notepad has been opened.")


    elif 'type' in voice_data:
        reply('What should I type?')
        text = record_audio()
        app.eel.addUserMsg(text)
        keyboard.type(text)
        reply('Text typed successfully')

    elif "set timer" in voice_data:
            # get the timer duration from the voice command
            duration = int(voice_data.split()[-2])

            # set the timer
            reply("Timer set for " + str(duration) + " seconds.")
            time.sleep(duration)
            reply("Timer finished.")

    elif 'play' in voice_data:
        song = voice_data.split('play')[-1]
        reply('Playing ' + song)
        pyautogui.press('playpause')

    elif 'pause' in voice_data:
        reply('Paused')
        pyautogui.press('playpause')

    elif 'volume up' in voice_data:
        reply('Increased Volume')
        pyautogui.press('volumeup')

    elif 'volume down' in voice_data:
        reply('Decreased Volume')
        pyautogui.press('volumedown')

    elif 'mute' in voice_data:
        reply('Muted')
        pyautogui.press('volumemute')

    elif 'scroll up' in voice_data:
        reply('Scrolling up')
        pyautogui.scroll(200)

    elif 'scroll down' in voice_data:
        reply('Scrolling down')
        pyautogui.scroll(-200)

    elif 'read' in voice_data:
        article = voice_data.split('read')[-1]
        reply('Searching...')
        result = wikipedia.summary(article, sentences=2)
        reply(result)
        
    
    elif 'what is your name' in voice_data:
        reply('My name is jarvis!')

    elif 'date' in voice_data:
        reply(today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply(str(datetime.datetime.now()).split(" ")[1].split('.')[0])

    elif 'search' in voice_data:
        reply('Searching for ' + voice_data.split('search')[1])
        url = 'https://google.com/search?q=' + voice_data.split('search')[1]
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif 'location' in voice_data:
        reply('Which place are you looking for ?')
        temp_audio = record_audio()
        app.eel.addUserMsg(temp_audio)
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')

    elif ('bye' in voice_data) or ('by' in voice_data) or ('bhai' in voice_data):
        reply("Good bye Sir! Have a nice day.")
        is_awake = False

    elif ('exit' in voice_data) or ('terminate' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        
        sys.exit()
        
    

    elif 'launch' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active')
        else:
            gc = Gesture_Controller.GestureController()
            t = Thread(target = gc.start)
            t.start()
            reply('Launched Successfully')

    elif ('stop gesture' in voice_data) or ('top gesture ' in voice_data):
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped')
        else:
            reply('Gesture recognition is already inactive')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
        
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
        

    elif 'list' in voice_data:
        counter = 0 
        path = 'C://'
        files = listdir(path)
        filestr = ""
        for f in files:
            counter+=1
            print(str(counter) + ':  ' + f)
            filestr += str(counter) + ':  ' + f + '<br>'
        file_exp_status = True
        reply('These are the files in your root directory')
        app.ChatBot.addAppMsg(filestr)
        
    elif file_exp_status == True:
        counter = 0   
        if 'open' in voice_data:
            if isfile(join(path,files[int(voice_data.split(' ')[-1])-1])):
                os.startfile(path + files[int(voice_data.split(' ')[-1])-1])
                file_exp_status = False
            else:
                try:
                    path = path + files[int(voice_data.split(' ')[-1])-1] + '//'
                    files = listdir(path)
                    filestr = ""
                    for f in files:
                        counter+=1
                        filestr += str(counter) + ':  ' + f + '<br>'
                        print(str(counter) + ':  ' + f)
                    reply('Opened Successfully')
                    app.ChatBot.addAppMsg(filestr)
                    
                except:
                    reply('You do not have permission to access this folder')
                                    
        if 'back' in voice_data:
            filestr = ""
            if path == 'C://':
                reply('Sorry, this is the root directory')
            else:
                a = path.split('//')[:-2]
                path = '//'.join(a)
                path += '//'
                files = listdir(path)
                for f in files:
                    counter+=1
                    filestr += str(counter) + ':  ' + f + '<br>'
                    print(str(counter) + ':  ' + f)
                reply('ok')
                app.ChatBot.addAppMsg(filestr)
                   
    else: 
        reply('I am not functioned to do this !')



t1 = Thread(target = app.ChatBot.start)
t1.start()


while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None
while True:
    if app.ChatBot.isUserInput():
        
        voice_data = app.ChatBot.popUserInput()
    else:
      
        voice_data = record_audio()


    if 'jarvis' in voice_data:
        try:
         
            respond(voice_data)
        except SystemExit:
            reply("Exit Successfull")
            break
        except:

            print("EXCEPTION raised while closing.") 
            break
        


