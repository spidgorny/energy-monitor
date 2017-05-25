from pprint import pprint

import numpy as np
import cv2
import argparse

from Canny import Canny
from Image.Pipeline import Pipeline


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

        knn = cv2.ml.KNearest_create()
        knn.load('ocr.knn')

        ret, results, neighbours, dist = knn.findNearest([digits], 5)
        pprint(ret, results, neighbours, dist)

o = OCR()
o.render()
