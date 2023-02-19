import cv2, numpy as np
import mediapipe as mp
import time

facedetect = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
video = cv2.VideoCapture(-1)

count = 0

if not video.isOpened():
    raise IOError("Cannot open webcam")


with facedetect.FaceDetection(min_detection_confidence=0.7) as face_detection:
    while video.isOpened():
        success, img = video.read()
        img = cv2.resize(img, (640, 480))
        #cv2.imshow("Normal", img)
        if success:
            count += 30 # i.e. at 30 fps, this advances one second
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detection.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if results.detections:
                for id, detection in enumerate(results.detections):
                    #mp_draw.draw_detections(img, detection)
                    xmin = round(detection.location_data.relative_bounding_box.xmin * 640)
                    ymin = round(detection.location_data.relative_bounding_box.ymin * 480)
                    cv2.rectangle(img,(xmin, ymin),(xmin + round(detection.location_data.relative_bounding_box.width * 640), ymin + round(detection.location_data.relative_bounding_box.height * 480) ),(0,255,0),2)
                    print(detection.location_data.relative_bounding_box)
                    print("DETECTED")

            cv2.imshow("fACE", img)
            #time.sleep(0.1)
        else:
            cap.release()
            break
        if cv2.waitKey(1) == ord("q"):
            break

video.release()
cv2.destroyAllWindows()




