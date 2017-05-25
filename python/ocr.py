from pprint import pprint

import numpy as np
import cv2
import argparse
import pickle
from Canny import Canny
from Image.Pipeline import Pipeline
from PIL import Image


class OCR:

    def __init__(self):
        parser = argparse.ArgumentParser(description='OCR numbers from <file>.')
        parser.add_argument('filename', metavar='filename', type=str,
                            help='image file to OCR from')

        args = parser.parse_args()
        filename = args.filename
        # print('filename', filename)
        if not filename:
            parser.print_help()
        else:
            self.filename = filename

    def render(self):
        p = Pipeline(self.filename)
        straight, edges, contimage, isolated, digits = p.process()

        # knn = cv2.ml.KNearest_create()
        # knn.load('ocr.knn')
        # ret, results, neighbours, dist = knn.findNearest([digits], 5)
        # pprint(ret, results, neighbours, dist)

        with open('ocr.svm', 'rb') as pickle_file:
            clf = pickle.load(pickle_file)

        samples = np.zeros((0, 450))
        for d in digits:
            d30 = cv2.resize(d, (15, 30), interpolation=cv2.INTER_LANCZOS4)
            gray = cv2.cvtColor(d30, cv2.COLOR_BGR2GRAY)
            features = np.reshape(gray, 450)
            samples = np.append(samples, [features], 0)

        res = clf.predict(samples)
        print(res)

        img = Image.open(self.filename)
        img.show()

o = OCR()
if o.filename:
    o.render()
