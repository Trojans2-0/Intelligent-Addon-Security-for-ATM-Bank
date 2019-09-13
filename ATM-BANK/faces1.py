import numpy as np
import cv2
import pickle
import sqlite3
from tkinter import *
from tkinter import messagebox

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')
upper_body=cv2.CascadeClassifier('cascades/data/haarcascade_upperbody.xml')
global flag
global get

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)
flag=1
while(flag):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5)
    eye=eye_cascade.detectMultiScale(gray,scaleFactor=1.5)

    for (x, y, w, h) in faces:
    	#print(x,y,w,h)
    	roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
    	roi_color = frame[y:y+h, x:x+w]
    	color = (255, 0, 0) #BGR 0-255 
    	stroke = 2
    	end_cord_x = x + w
    	end_cord_y = y + h
    	cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        

    	# recognize? deep learned model predict keras tensorflow pytorch scikit learn
    	id_, conf = recognizer.predict(roi_gray)
    	if conf>=4 and conf <= 55:
    		#print(5: #id_)
    		get=labels[id_]
    		flag=0
    		font = cv2.FONT_HERSHEY_SIMPLEX
    		name = labels[id_]
    		color = (255, 255, 255)
    		stroke = 2
    		cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

    	img_item = "sample.png"
    	cv2.imwrite(img_item, roi_color)

    	

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & flag == 0 :
        break
con=sqlite3.connect('images.db')
cursor=con.cursor()
name='IMAGE'
cursor.execute("""CREATE TABLE IF NOT EXISTs ImageTable (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,data BLOB)""")
with open ('sample.png','rb') as f:
    data=f.read()
cursor.execute(""" INSERT INTO ImageTable (name,data) VALUES (?,?)""",(name,data))
con.commit()
cursor.close()
con.close()
if get=="human_face":
    roots = Tk() 
    roots.title('verify')
    intruction = Label(roots, text='BANK TRANSACTION:')
    intruction.grid(row=0, column=0, sticky=E)
 
    nameL = Label(roots, text='Account Number  :') 
    nameL.grid(row=1, column=0)
    nameL1 = Label(roots, text='CVV   :')
    nameL1.grid(row=3, column=0)
    nameL2 = Label(roots, text='PIN   :')
    nameL2.grid(row=5, column=0)
 
    nameE = Entry(roots)
    nameE.grid(row=1, column=3)
    nameE2 = Entry(roots)
    nameE2.grid(row=3, column=3)
    nameE1 = Entry(roots)
    nameE1.grid(row=5, column=3)
    roots.geometry("600x400")
    
    messagebox.showinfo("Insertion","Please Insert Your Credit Card....")


    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
