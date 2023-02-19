from multiprocessing import Process
import threading
from pubsub import pub
import serial
import queue
import mediapipe as mp
import cv2, numpy as np
import threading


import os
from time import time, sleep

# Import Python files
from oled_controller import oledController
from arduino_controller import arduinoController # Works
from camera_controller import cameraController
#from speaker_controller import oledController
#from aCap import VideoStream


def came():
    cameraController().update()



def main():

    oledControl = oledController()   # Create OLED controller class object
    arduinoControl = arduinoController()   # Create Arduino controller class object
    cameraControl = threading.Thread(target=came).start
    #camera = VideoStream()
    
    # Establish serial connection via USB with arduino
    # Needed for arduino controller class
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    except:
        ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
        pass
    ser.reset_input_buffer()   # Reset serial stream in caseof any garbage left behind
    
    # Start timer for different loops and set looping to true
    second_loop = time()
    ten_second_loop = time()
    loop = True
    
    #pub.subscribe(oled_control, "motor")
    
    while loop:
        
        if time() - second_loop > 1:   # If the time takeaway the second_loop time is less than a second do this
            second_loop = time()   # Set new time
            print("second")   # Print this
            
        if time() - ten_second_loop > 2:    # If the time takeaway the ten_second_loop time is less than a second do this
            ten_second_loop = time()   # Set new time
            pub.sendMessage("cameraTrack", ser=ser, angle1 = 60, angle2 = 140)   # publish message 'cameraTrack' with arguements. This is recieved by the arduino controller class listener
            #pub.sendMessage("emotion", arg ={'emotion': 3})
            print("ten seconds")
        
    video.release()
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    