# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import tkinter as tk
from tkinter import *
from datetime import datetime
from PIL import Image
import sqlite3
import multiprocessing as mp
import os, fnmatch
import re
import smtplib, ssl
import random
import tkinter as tk
from tkinter import *





#CREATING DATABASE OR CONNECTING 
logdb=sqlite3.connect("login.db")

#create cursor
c=logdb.cursor()



def filecreate():

        try:
                today=time.strftime('%Y_%m_%d')
                str(today)
                global path
                path =("pwom/_"+today)
                os.mkdir(path)
        except FileExistsError:
                print("File already exists!!!")
                print("Fetching FILE....")

filecreate()

##def fileimg(label):
##	if label=="No Mask":
##		import face_recognition
##		#time.sleep(5)
##		now=time.strftime('%H_%M_%S')
##		for nm in range(1):
##			cv2.imwrite(os.path.join(path , str(now)+'.png'), img)
##			nm+=1
##			break
def fileimg(label,img):
        if label=="No Mask":
                


                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(r'facerecog\trainer\trainer.yml')
                cascadePath = r"facerecog\haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(cascadePath);

                font = cv2.FONT_HERSHEY_SIMPLEX

                #iniciate id counter
                id = 0

                # names related to ids: example ==> Marcelo: id=1,  etc
                #names = ['None', 'end','Admin','TEJAS','Shivam','HARAL']
                c.execute("SELECT userid FROM usrinfo ")
                names = c.fetchall()
                list(names)
                names.insert(0,'none')
                
                while True:

                        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                        faces = faceCascade.detectMultiScale( 
                        gray,
                        scaleFactor = 1.2,
                        minNeighbors = 5,
                        )
                        for(x,y,w,h) in faces:

                                #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                                i =  0
                                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                                # Check if confidence is less them 100 ==> "0" is perfect match 
                                if (confidence < 100):
                                        id1 = names[id]
                                        confidence = "  {0}%".format(round(100 - confidence))
                                else:
                                    id1 = "unknown"+str(i)
                                    confidence = "  {0}%".format(round(100 - confidence))

                                cv2.putText(img, str(names[id]), (x+5,y-5), font, 1, (255,255,255), 2)
                                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                                now=time.strftime('%H_%M_%S')


                                
                                listoffiles = os.listdir("pwom")
                                for tofolder in reversed(listoffiles):
                                        print(tofolder)
                                        break
                                #to check file name is same or not
                                pattern = "*"+str(id1)+".png"
                                un="unknown"+str(i)+".png"
                                tofolder=str(tofolder[1:])
                                #entering latest directory
                                fold = "pwom/_"+tofolder
                                folder = os.listdir(fold)
                                
                                if len(folder) > 0:
                                        for file in folder:
                                                if fnmatch.fnmatch(file,un):
                                                                print("unknown")
                                                                cv2.imwrite(os.path.join(path , str(now)+'_'+str(id1)+'.png'), img)
                                                                i+=1
                                                                break
                                                elif not fnmatch.fnmatch(file,pattern):
                                                                print("known")
                                                                print(names[id])
                                                                cv2.imwrite(os.path.join(path , str(now)+'_'+str(id1)+'.png'), img)
                                                                i+=1
                                                                # create smtp session 
                                                                s = smtplib.SMTP("smtp.gmail.com" , 587)  # 587 is a port number
                                                                # start TLS for E-mail security 
                                                                s.starttls()
                                                                # Auto Log in to your gmail account
                                                                s.login("g9fmds09@gmail.com" , "G9FMDS@fmds09")
                                                                #send email
                                                                subject = 'Mask Detection System'
                                                                body = 'Mask Not Detected, Please Wear A mask Before Entering Premises.'
                                                                passfor = "\n Thank you"
                                                                c.execute("SELECT email FROM usrinfo WHERE userid = ?;",names[id])
                                                                email = c.fetchall()
                                                                msg = f'Subject: {subject}\n\n{body}\n{passfor}'
                                                                s.sendmail("g9fmds09@gmail.com" , email,msg)
                                                                print("Email sent succesfully..")
                                                                break
                                                else:
                                                        break
                                        break
                                else:
                                        cv2.imwrite(os.path.join(path , str(now)+'_'+str(id)+'.png'), img)



                        break

                # Do a bit of cleanup
                print("\n [INFO] Exiting Program and cleanup stuff")

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	print(detections.shape)

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model( r"mask_detector.model")

ipvar3= "http://192.168.31.81:4747/video"

# initialize the video stream
print("[INFO] starting video stream...")

#vs = VideoStream(src=0).start()
vs = VideoStream(ipvar3).start()


# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	global frame,label
	frame = vs.read()

	frame = imutils.resize(frame, width=400)

	# detect faces in the frame and determine if they are wearing a
	# face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# loop over the detected face locations and their corresponding
	# locations
	for (box, pred) in zip(locs, preds):
			# unpack the bounding box and predictions
			(startX, startY, endX, endY) = box
			(mask, withoutMask) = pred
			# determine the class label and color we'll use to draw
			# the bounding box and text
			label = "Mask" if mask > withoutMask else "No Mask" 
			color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

			fileimg(label,frame) if label == "Mask" else fileimg(label,frame) 

			# include the probability in the label
			label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

			# display the label and bounding box rectangle on the output
			# frame
##			cv2.putText(frame, label, (startX, startY - 10),
##				cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		
	# show the output frame
	
	cv2.imshow("Frame", frame)
		
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		cv2.destroyAllWindows()
		vs.stop()
		break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
