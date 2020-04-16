import cv2
import numpy as np
import os 
import pyttsx3
import time
def recognise():
    
    engine = pyttsx3.init("sapi5")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('model.h5')   #load trained model
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    voices = engine.getProperty('voices')
    engine.setProperty("rate", 180)
    engine.setProperty('voice', voices[0].id)
    engine.say("Welcome to the game, Press, A, for face identification or, q, to quit")
    
    
    f=open("id.txt","r+")
    a=f.readline()
    a=int(a)
    id = a 
    print(id)
    
    names = []
    with open("names.txt") as f:
        for line in f:
            names.append(line.rstrip('\n'))
    print(names)
   
    cam = cv2.VideoCapture(0)
    cam.set(3, 1024) # set video widht
    cam.set(4, 768) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    found=False
    start=False
    engine.runAndWait()
    while True:

        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.rectangle(img, (0,0), (1024,100), (255,0,0),-1)
        cv2.putText(img, "Press 'A' to Start..", (95,50), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255), 2)
        
        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
                )
        
        if(start):
        
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (0,0), (1024,100), (255,0,0),-1)
                cv2.putText(img, "Detecting Faces..", (95,50), font, 2,(0,0,255), 2)
                #time.sleep(4)
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 75):
                    found=True
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    #cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                    #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 
                    cv2.putText(img, "Welcome "+str(id), (300,500), font, 1,(0,0,255), 2)
                    cv2.rectangle(img, (0,0), (1024,100), (255,0,0),-1)
                    cv2.putText(img, "Detecting Faces..", (95,50), font, 2,(0,0,255), 2)
                    cv2.putText(img, "Welcome "+str(id), (300,500), font, 1,(0,0,255), 2)
                    engine.say("Welcome, "+str(id))
                    engine.runAndWait()
                
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10)
        if (k == ord('a')):
            start = not start
        
        if(found==True or k==ord('q')):    
            break
    

# Do a bit of cleanup
    print("\nReleasing camera")
    cam.release()
    cv2.destroyAllWindows()
    return id
#recognise()
