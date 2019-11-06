### Open CV + Flask Tests
import cv2
import numpy as np
from flask import *

app = Flask (__name__)
@app.route ("/")
def hello():
    #cap = cv2.VideoCapture ("http://172.19.11.69:9000/?action=stream")
    cap = cv2.VideoCapture (0)
    cap.set (3, 100)
    cap.set (4, 100)

    while cap.isOpened():
        ret, frame = cap.read() # ret is true or false statement
    
        if ret:
            framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 100, 100)
            edges = cv2.Canny(frame, 100, 100)
            im2, contours, hierarchy = cv2.findContours (edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect (contour)
                if w>20 and h>20:
                    cv2.rectangle (frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    print ("OBJECT DETECTED!")
                    status = "Object Detected"
                else:
                    status = "Clear Path"
                return render_template('hello.html', status = status)
    
            cv2.imshow ("original", frame)
            if cv2.waitKey (1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

#app = Flask (__name__)
#@app.route ("/")
#def hello():
#    while 1:
#        object = raw_input ("Is there an object in the way? ")
#        if object == "yes":
#            status = "Object Detected"
#        else:
#            status = "Go for it mateeeee"
#        return render_template('hello.html', status = status)
