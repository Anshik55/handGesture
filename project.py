import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import numpy as np
import screen_brightness_control as sbc

cap=cv2.VideoCapture(0)                                         #it opens the window in which you can give gestures

mpHands=mp.solutions.hands                                      # It is used for framing the hand. A hand landmark model that operates on the
hands=mpHands.Hands()                                           # cropped image region defined by the palm detector and returns 
mpDraw=mp.solutions.drawing_utils                               # high-fidelity 3D hand keypoints.

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume=cast(interface, POINTER(IAudioEndpointVolume))

volMin,volMax=volume.GetVolumeRange()[:2]                       # here we are getting the volume range 

print("\n*****************************************************************************\n")

print("\n Welcome to the AI project \n")

print("\n*****************************************************************************\n")

print("Enter 1 for volume control \n"+
    "\nEnter 2 for brightness control\n")

n=int(input())
print("\n*****************************************************************************\n")

temp=True

while temp==True:
    if n==1 or n==2:

        while True:
            s,img=cap.read()                                       # we are capturing the image here
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)             # color of image is being converted
            results=hands.process(imgRGB)

            lmList=[]
            if results.multi_hand_landmarks:
                for handlandmark in results.multi_hand_landmarks:
                    for id,Im in enumerate(handlandmark.landmark):
                        h,w,_=img.shape
                        cx,cy=int(Im.x*w),int(Im.y*h)
                        lmList.append([id,cx,cy])
                    mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

            if lmList!=[]:
                x1,y1=lmList[4][1],lmList[4][2]
                x2,y2=lmList[8][1],lmList[8][2]

                cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)      # this funtion is used to draw circle on the index finger 
                cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)      # this funtion is used to draw circle on the thumb
                cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)           # this function draws line between thumb and index finger

                length=hypot(x2-x1,y2-y1)                           # this function returns the hypotenuse of traingle made by the arguments

                if n==1:

                    vol=np.interp(length,[15,220],[volMin,volMax])  # this is the main function for volume control     
                    print(vol,length)                               # here volume is being changed acccording the interp functions 
                    volume.SetMasterVolumeLevel(vol,None)           # arguments. length is the arguments which will changand volume accordingly.

                elif n==2:

                    bright=np.interp(length,[15,220],[0,100])       # here brighntess is being changed.  
                    print(bright,length)                            # this print is printing the realtime coordinates 
                    sbc.set_brightness(int(bright))                    

            cv2.imshow('Image',img)                                 # it is used to display an image in a window
            if cv2.waitKey(1) & 0xff==ord('q' or 'Q'):
                break

        temp=False

    else:
        print("Enter valid options!!!")
        print("Enter 1 for volume control\n"+
        "Enter 2 for brightness control..")
        n=int(input())
