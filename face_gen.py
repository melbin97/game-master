import cv2
import os

f=open("id.txt","r+")
fh=open("names.txt","a+")

fline=f.readline()
a=int(fline)
a=a+1
print("Id assigned is ",a)
name=input("Enter your name?")

id = str(a)

IMG_SAVE_PATH = 'users'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, 's'+id)

try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass

try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")

cap=cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count=0;
start = False

while(True):
    ret,frame=cap.read()
    frame = cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.1,4)
    if start:
        for (x, y, w, h) in faces:
            count=count+1;
            save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count))
            cv2.imwrite(save_path, gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if count>200:
            f.seek(0)
            f.writelines(str(a))
            fh.write(name)
            fh.close()
            f.close()
            break
    cv2.imshow('frame',frame)
    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


    