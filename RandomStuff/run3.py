
import cv2
#loading pre trained face data from opencv
trained_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#grabbing webcam 
webcam = cv2.VideoCapture(0)

while True:
    #reading webcam frames
    frame_read,frame = webcam.read()
    frame = cv2.resize(frame, (480, 360))
    greyscale_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face_cordinates = trained_data.detectMultiScale(greyscale_frame)
    #x and y is the upper left corner coordinate and w and h are the corresponding width and height of the rectangle
    for (x,y,w,h) in face_cordinates:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("Anil's Face Detection App",frame)
    #agument 1 defines milliseconds
    cv2.waitKey(1) # keeps imaage in the screen