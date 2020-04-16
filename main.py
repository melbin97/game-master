import sys
import os
import face_recog
import pyttsx3
#import cv2
engine = pyttsx3.init("sapi5")
sys.path.append('gestures')
#import dummy
#os.chdir('..')
cwd = os.getcwd()
print(cwd)
#cam = cv2.VideoCapture(0)
a=face_recog.recognise()

from threading import Thread
def myfunc():
    voices = engine.getProperty('voices')
    engine.setProperty("rate", 150)
    engine.setProperty('voice', voices[1].id)
    engine.say("Okay then, let's start the game")
    engine.runAndWait()
t = Thread(target=myfunc)
t.start()
os.chdir('gestures')
import dummy
dummy.game()