import numpy as np
import cv2
import pickle

from Image.PipelineVideo import PipelineVideo

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(len(frame));

    # Display the resulting frame
    # cv2.imshow('frame', frame)

    p = PipelineVideo(frame)
    straight, edges, contimage, isolated, digits = p.process()
    print(len(digits))
    samples = p.resizeReshape(digits)
    print(len(samples))

    with open('ocr.snn', 'rb') as pickle_file:
        clf = pickle.load(pickle_file)
        print(clf)

    res = clf.predict(samples)
    print('res', res)

    cv2.waitKey(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

dict = []
dict.append()
