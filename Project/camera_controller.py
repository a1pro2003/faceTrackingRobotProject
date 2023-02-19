import cv2, numpy as np
import mediapipe as mp
import time
import threading
#from arduino_controller import arduinoController # Works
from pubsub import pub
import serial
from math import sqrt
import paho.mqtt.client as mqtt


from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__)
#video = cv2.VideoCapture(0)

#client.publish("arduino","ON")

def run():
    time.sleep(0.3)
    facedetect = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils
    video = cv2.VideoCapture(-1)
    count = 0
    
    angle1 = 100
    angle2 = 100
    

    if not video.isOpened():
        print(IOError("Cannot open webcam"))
        video = cv2.VideoCapture(-1)

    n = 0

    with facedetect.FaceDetection(min_detection_confidence=0.7) as face_detection:
        while video.isOpened():
            #client.publish("arduino", "nice")
            success, img = video.read()
            fwidth, fheight = 600, 480
            fwmid, fhmid = fwidth/2, fheight/2
            img = cv2.resize(img, (fwidth, fheight))
            #cv2.imshow("Normal", img)
            
            if success:
                count += 60 # i.e. at 30 fps, this advances one second
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = face_detection.process(img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                if results.detections:
                    for id, detection in enumerate(results.detections):
                        #mp_draw.draw_detections(img, detection)
                        xmin = round(detection.location_data.relative_bounding_box.xmin * fwidth)
                        ymin = round(detection.location_data.relative_bounding_box.ymin * fheight)
                        cv2.rectangle(img,(xmin, ymin),(xmin + round(detection.location_data.relative_bounding_box.width * 600), ymin + round(detection.location_data.relative_bounding_box.height * 480) ),(0,255,0),2)
                        #print(detection.location_data.relative_bounding_box)
                        cv2.line(img, (xmin+round(detection.location_data.relative_bounding_box.width/2 * fwidth),ymin + round(detection.location_data.relative_bounding_box.height/2 * fheight)), (300, 240), (255,0,255))
                        
                        square_size = xmin + round(detection.location_data.relative_bounding_box.width * 600) - xmin
                        line_length_x = (xmin+round(detection.location_data.relative_bounding_box.height/2 * fwidth)) - fwmid
                        line_length_y = (ymin+round(detection.location_data.relative_bounding_box.width/2 * fheight)) - fhmid
                        line_length = round(sqrt((line_length_x**2) + (line_length_y**2)))
                        print("square size: ", square_size)
                        print("x: ", line_length_x)
                        print("y: ", line_length_y)
                        print("line: ", line_length)
                        
                        
                        if n == 8:
                            strcommand = '{"xlength":'+f'{line_length_x}'+', "ylength":'+f'{line_length_y}'+', "squaresize":'+f'{square_size}'+', "linelength":'+f'{line_length}'+'}'
                            print(strcommand)
                            client.publish("arduino", strcommand)
                            
                            client.loop()
                            n = 0
                        n = n + 1
                        print(n)
                        #pub.sendMessage("cameraTrack", ser=ser, angle1 = 20, angle2 = 100)
                        print("DETECTED")
 
                cv2.circle(img, (int(fwmid), int(fhmid)), 2, (0,0,255))
                img = cv2.flip(img, 0)
                # cv2.imshow("fACE", img)
                #time.sleep(0.1)
            else:
                cap.release()
                break
            if cv2.waitKey(1) == ord("q"):
                break
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    video.release()
    cv2.destroyAllWindows()


#run()


@app.route('/video_feed')
def video_feed():
    global video
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(run(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/f', methods=['GET', 'POST'])
def f():
    time.sleep(0.1)
    comm = '{"dirr":1, "sped":2, "secs":1}'
    client.publish("arduino", comm)
    time.sleep(0.1)    
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/b', methods=['GET', 'POST'])
def b():
    time.sleep(0.1)
    comm = '{"dirr":2, "sped":2, "secs":1}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/r', methods=['GET', 'POST'])
def r():
    time.sleep(0.1)
    comm = '{"dirr":3, "sped":2, "secs":1}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/l', methods=['GET', 'POST'])
def l():
    time.sleep(0.1)
    comm = '{"dirr":4, "sped":2, "secs":1}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/s', methods=['GET', 'POST'])
def s():
    time.sleep(0.1)
    comm = '{"dirr":0, "sped":2, "secs":1}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')


@app.route('/up', methods=['GET', 'POST'])
def up():
    time.sleep(0.1)
    comm = '{"reset": 0, "up": 1, "down": 0, "right": 0, "left": 0}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/down', methods=['GET', 'POST'])
def down():
    time.sleep(0.1)
    comm = '{"reset": 0, "up": 0, "down": 1, "right": 0, "left": 0}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/right', methods=['GET', 'POST'])
def right():
    time.sleep(0.1)
    comm = '{"reset": 0, "up": 0, "down": 0, "right": 1, "left": 0}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/left', methods=['GET', 'POST'])
def left():
    time.sleep(0.1)
    comm = '{"reset": 0, "up": 0, "down": 0, "right": 0, "left": 1}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    time.sleep(0.1)
    comm = '{"reset": 1, "up": 0, "down": 0, "right": 0, "left": 0}'
    client.publish("arduino", comm)
    time.sleep(0.1)
    #Video streaming route. Put this in the src attribute of an img tag
    return render_template('in.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
#    if request.method == 'POST':
 #       while True:
  #          if request.form.get('action1') == 'F':
   #             comm = '{"dirr":1, "sped":2, "secs":1}'
    #            client.publish("arduino", comm)
     #           break
      #      
       #     elif request.form.get('action2') == 'B':
        #        comm = '{"dirr":2, "sped":2, "secs":1}'
         #       client.publish("arduino", comm)
          #      break
           # 
 #           elif request.form.get('action3') == 'R':
#                comm = '{"dirr":3, "sped":2, "secs":1}'
  #              client.publish("arduino", comm)
   #             break
    #            
     #       elif request.form.get('action4') == 'L':
      #          comm = '{"dirr":4, "sped":2, "secs":1}'
       #         client.publish("arduino", comm)
        #        break
         ##       
           # elif request.form.get('action0') == 'S':
            #    comm = '{"dirr":0, "sped":2, "secs":1}'
             #   client.publish("arduino", comm)
              #  break
 #           elif request.form.get('actionCam1') == 'Cam Up':
  #              comm = '{"reset": 0, "up": 1, "down": 0, "right": 0, "left": 0}'
   #             client.publish("arduino", comm)
   #             break
    #        elif request.form.get('actionCam2') == 'Cam Down':
      #          comm = '{"reset":0, "up": 0, "down": 1, "right": 0, "left": 0}'
       #         client.publish("arduino", comm)
         #       break
 #           elif request.form.get('actionCam3') == 'Cam Right':
  #              comm = '{"reset":0, "up": 0, "down": 0, "right": 1, "left": 0}'
   #             client.publish("arduino", comm)
    #            break
     #       elif request.form.get('actionCam4') == 'Cam Left':
      #          comm = '{"reset":0, "up": 0, "down": 0, "right": 0, "left": 1}'
       #         client.publish("arduino", comm)
        #        break
         #   elif request.form.get('actionCam0') == 'Reset View':
          #      comm = '{"reset":1, "up": 0, "down": 0, "right": 0, "left": 0}'
           #     client.publish("arduino", comm)
            #    break
         #   else:
           #     pass # unknown
    #if request.method == 'GET':
     #   return render_template('in.html')
    #time.sleep(0.2)
    return render_template('in.html')


if __name__ == '__main__':
    client = mqtt.Client('client_2')
    client.connect('0.0.0.0', port=1883, keepalive=60, bind_address="")
    client.loop_start()
   # video = cv2.videoCapture(0)
    app.run(debug=True, host="0.0.0.0", port=1234)




