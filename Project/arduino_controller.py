from pubsub import pub
import serial
from time import sleep
import json
import ast
import paho.mqtt.client as mqtt
import math
import time
#from oled_controller import oledController


client = mqtt.Client('client_23421')

#client.publish("arduino","ON")



class arduinoController:
    
    def __init__(self): # Initiate class 
        #ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        #ser.reset_input_buffer()
        self.elbowAngle = 50 # Set starting position for the elbow servo
        self.baseAngle = 90 # Set starting position for base servo
        #pub.subscribe(self.moveCamera, "cameraTrack") # susbcribe to 'cameraTrack' topic and execute moveCamera
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        except:
            self.ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
            pass
        self.ser.reset_input_buffer()
        sleep(1)
        self.moveCamera(self.ser, 90, 40)
        self.animationOn = 0
        self.hit = 0
        #self.oledControl = oledController()   # Create OLED controller class object

        print("nice")
        
    def decodeData(self, client, userdata, message):
        try:
            #client.loop()
            string = str(message.payload.decode("utf-8"))
            print(string)
            jsonstring = json.loads(string)
            xlength = int(jsonstring["xlength"])
            ylength = int(jsonstring["ylength"])
            linelength = int(jsonstring["linelength"])
            squaresize = int(jsonstring["squaresize"])

            if xlength >= 50 or xlength <= -50 :
                if  xlength <= 0 and (self.baseAngle - 10) >= 0:
                    self.baseAngle = self.baseAngle - 10
                if xlength >= 0 and (self.baseAngle + 10) <= 180:
                    self.baseAngle = self.baseAngle + 10
            
            if ylength >= 40 or ylength <= -40 :
                if  ylength <= 0 and (self.elbowAngle - 5) >= 0:
                    self.elbowAngle = self.elbowAngle - 5
                if ylength >= 0 and (self.elbowAngle + 5) <= 90:
                    self.elbowAngle = self.elbowAngle + 5
                     
            if linelength <= 70 and self.animationOn == 0:
                #pub.sendMessage("emotion", arg ={'emotion': 1})
                client.publish("emotion", '{"emotion": 4}')
                self.animationOn = 1
            
                
            if linelength >= 100 and self.animationOn == 0:
                client.publish("emotion", '{"emotion": 5}')
                self.animationOn = 1
                
            if self.hit >= 4:
                self.hit = 0
                self.animationOn = 0
                
            self.hit = self.hit + 1
            
            print(squaresize)
            print("linelength: ",linelength)
            print("x: ",xlength)
            print("y: ",ylength)
            print("hits: ", self.hit)
            print("animation: ", self.animationOn)
            
            angle1 = self.baseAngle
            angle2 = self.elbowAngle
            self.moveCamera(self.ser, angle1, angle2)
            pass
        except Exception as error:
            print(error)
            print("error1")
                
        try:
            string = str(message.payload.decode("utf-8"))
            print(string)
            jsonstring = json.loads(string)
            reset = int(jsonstring["reset"])
            up = int(jsonstring["up"])
            down = int(jsonstring["down"])
            right = int(jsonstring["right"])
            left = int(jsonstring["left"])
            if reset == 1 :
                self.baseAngle = 90
                self.elbowAngle = 50
            elif up == 1:
                self.elbowAngle = self.elbowAngle + 5
            elif down == 1:
                self.elbowAngle = self.elbowAngle - 5
            elif right == 1:
                self.baseAngle = self.baseAngle + 10
            elif left == 1:
               self.baseAngle = self.baseAngle - 10
               
            angle1 = self.baseAngle
            angle2 = self.elbowAngle
            self.moveCamera(self.ser, angle1, angle2)
            pass
        
        except Exception as error:
            print(error)
            print("error2")
            
        try:
            string = str(message.payload.decode("utf-8"))
            print(string)
            jsonstring = json.loads(string)
            dirr = int(jsonstring["dirr"])
            sped = int(jsonstring["sped"])
            secs = int(jsonstring["secs"])
          #  print(dirr)
          #  print(sped)
           # print(secs)
            self.moveMotor(self.ser, dirr, sped, secs)
            pass
        
        except Exception as error:
            print(error)
            print("error3")
        
    def moveMotor(self, ser, dirr, sped, secs):
        message = '{"topic":["motor",{"motor": [{"id": 1, "dir": '+f'{dirr}'+', "sped": '+f'{sped}'+', "secs": '+f'{secs}'+'}]}]}\n'
        stop = '{"topic":["motor",{"motor": [{"id": 1, "dir": 0, "sped": 2, "secs": 1}]}]}\n'
        ser.write(message.encode('utf-8')) # encode String and write to serial port
        time.sleep(secs)
        ser.write(message.encode('utf-8'))
        print("success")
        try:
            line = ser.readline().decode('utf-8').rstrip() # Try to read the serial port ( not needed)
            #print(line) # Print serial port
            #jsonString = json.loads(line) # This turns the string into a JSON string from the serial port
            #print(jsonString["camera"][0]["angle"]) # Print a parameter from the json string
        except:
            pass
        
    def moveCamera(self, ser, angle1, angle2):
        #global elbowAngle, baseAngle
        #print("here")
        #if ser.in_waiting > 0:
        #['camera': {['id': 1, 'angle': 90], ['id':2, 'angle':90]}]
        #print(ser)
        self.elbowAngle = angle2 # Set angle1 to the elbow angle
        self.baseAngle = angle1 # Set angle2 to base angle
        print("base: ",angle1)
        print("elbow: ",angle2)
        message = '{"topic":["camera",{"camera": [{"id": 1, "angle": '+f'{self.elbowAngle}'+'}, {"id":2, "angle":'+f'{self.baseAngle}'+'}]}]}\n' # Format string with new angles. String is in JSON format for serial connection
        ser.write(message.encode('utf-8')) # encode String and write to serial port
        print("success")
        try:
            line = ser.readline().decode('utf-8').rstrip() # Try to read the serial port ( not needed)
            #print(line) # Print serial port
            #jsonString = json.loads(line) # This turns the string into a JSON string from the serial port
            #print(jsonString["camera"][0]["angle"]) # Print a parameter from the json string
        except:
            pass


arduino = arduinoController()
client.on_message = arduino.decodeData
client.connect('0.0.0.0', port=1883, keepalive=60, bind_address="")
client.loop_start()
client.subscribe('arduino')

#client.subscribe('emotion')
sleep(3)
#client.publish("arduino",'{"angle1":20,"angle2":80}')

while True:
    pass


