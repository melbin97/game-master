from keras.models import load_model
import cv2
import numpy as np
import os
import sys
import time
import markov
sys.path.append('gestures')
from random import choice
def game():  
    upoint=0
    cpoint=0
    REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
    }
    
    print(os.getcwd())
    def mapper(val):
        return REV_CLASS_MAP[val]
    
    model = load_model(r"C:\Users\melbi\game-master\gestures\rock-paper-scissors-model.h5")
    
    cap = cv2.VideoCapture(0)
    prev_move = None
    cap.set(3,1280)
    cap.set(4,720)
    
    while True:
         ret, frame = cap.read()
         frame=cv2.flip(frame,1)
         if not ret:
             continue

        # rectangle for user to play
         cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
        # rectangle for computer to play
         cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)
        
         # extract the region of image within the user rectangle
         roi = frame[100:500, 100:500]
         img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
         img = cv2.resize(img, (227, 227))
        
         # predict the move made
         pred = model.predict(np.array([img]))
         move_code = np.argmax(pred[0])
         user_move_name = mapper(move_code)
        
        # # predict the winner (human vs computer)
         if prev_move != user_move_name:
              if user_move_name != "none":
                #computer_move_name = choice(['rock', 'paper', 'scissors'])
                winner,computer_code = markov.markov(move_code)
                computer_move_name=mapper(computer_code)
                if(winner=="Win"):
                    upoint=upoint+1
                elif(winner=="Lose"):
                    cpoint=cpoint+1
                else:
                    pass
              else:
                  computer_move_name = "none"
                  winner = "Waiting..."
         prev_move = user_move_name
         # display the information
         font = cv2.FONT_HERSHEY_SIMPLEX
         cv2.putText(frame, "Your Move: " + user_move_name,(50, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
         cv2.putText(frame, "Your score: " + str(upoint),(50, 600), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
         cv2.putText(frame, "Computer's Move: " + computer_move_name,(750, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
         cv2.putText(frame, "Computer's Score: " + str(cpoint),(750, 600), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
         cv2.putText(frame, "Winner: " + winner,(400, 700), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
         
         if computer_move_name != "none":
             icon = cv2.imread("images/{}.png".format(computer_move_name))
             icon = cv2.resize(icon, (400, 400))
             frame[100:500, 800:1200] = icon
             
         cv2.imshow("Rock Paper Scissors", frame)
         k = cv2.waitKey(10)
         if k == ord('q'):
             break
    cap.release()
    cv2.destroyAllWindows()
#game()

