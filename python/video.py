import numpy as np
import cv2
import pickle

from Image.PipelineVideo import PipelineVideo

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    p = PipelineVideo(frame)
    straight, edges, contimage, isolated, digits = p.process()
    samples = p.resizeReshape(digits)

    with open('ocr.snn', 'rb') as pickle_file:
        clf = pickle.load(pickle_file)

    res = clf.predict(samples)
    print(res)

    cv2.waitKey(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
