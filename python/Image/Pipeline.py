import cv2
from os import path

import numpy as np

from Image.Cannify import Cannify
from Image.IsolateDigits import IsolateDigits
from Image.Straighten import Straighten


class Pipeline:

    def __init__(self, filename):
        self.file = filename
        self.img = cv2.imread(self.file, 0)
        self.height, self.width = self.img.shape
        """ :var Canny """
        self.cannify = None

    def process(self):
        straighten = Straighten(self.img)
        straight = straighten.process()

        edges = cv2.Canny(straight, 100, 200)

        self.cannify = Cannify(edges)
        contimage = self.cannify.process()
        contours = self.cannify.getDigits()

        isolated = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.drawContours(isolated, contours, contourIdx=-1, color=(255, 255, 255))
                         # thickness=cv2.FILLED)

        # alternatively fill the contours
        # todo: this does not let openings
        # for c in contours:
        #     cv2.fillPoly(isolated, pts=[c], color=(255, 255, 255))

        isolator = IsolateDigits(isolated)
        digits = isolator.isolate(contours)

        return straight, edges, contimage, isolated, digits
