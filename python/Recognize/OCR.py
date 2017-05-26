import argparse
import pickle
import random
from os import listdir
from os import path
from pprint import pprint

import cv2
import numpy as np
from PIL import Image

from Image.Pipeline import Pipeline


class OCR:
    def __init__(self):
        parser = argparse.ArgumentParser(description='OCR numbers from <file>.')
        parser.add_argument('filename', metavar='filename', type=str, nargs='?',
                            help='image file to OCR from')

        args = parser.parse_args()
        filename = args.filename
        # print('filename', filename)
        if not filename:
            self.mypath = '../cache/';
            onlyfiles = [f for f in listdir(self.mypath)
                         if path.isfile(path.join(self.mypath, f))]
            file = random.choice(onlyfiles)
            self.filename = path.join(self.mypath, file)
        else:
            self.filename = filename

    def render(self):
        p = Pipeline(self.filename)
        straight, edges, contimage, isolated, digits = p.process()
        samples = p.resizeReshape(digits)

        knn = False
        svc = False
        gnb = False
        snn = True
        if knn:
            knn = cv2.ml.KNearest_create()
            knn.load('ocr.knn')  # <- this method does not exist
            ret, results, neighbours, dist = knn.findNearest([digits], 5)
            pprint(ret, results, neighbours, dist)
        elif svc:
            with open('ocr.svm', 'rb') as pickle_file:
                clf = pickle.load(pickle_file)

            res = clf.predict(samples)
            print(res)

            img = Image.open(self.filename)
            img.show()
        elif gnb:
            with open('ocr.gnb', 'rb') as pickle_file:
                clf = pickle.load(pickle_file)

            res = clf.predict(samples)
            print(res)

            img = Image.open(self.filename)
            img.show()

        elif snn:
            with open('ocr.snn', 'rb') as pickle_file:
                clf = pickle.load(pickle_file)

            res = clf.predict(samples)
            print(res)

            img = Image.open(self.filename)
            img.show()
