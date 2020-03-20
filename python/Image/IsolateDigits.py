import cv2

from Image.Cannify import Cannify
from .ImageProcessor import ImageProcessor
import random
import numpy as np
import math


class IsolateDigits(ImageProcessor):
    """
    We could use findContours() on the image again, but we have contours already
    Give up
    https://stackoverflow.com/questions/29523177/opencv-merging-overlapping-rectangles
    """

    def __init__(self, img):
        super().__init__(img)

    def isolate(self, contours):
        digits = []
        # must be RETR_EXTERNAL this time
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

        # remove tiny specs which happen to fit bounding box of big characters
        contimage = np.zeros((self.height, self.width, 3), np.uint8)
        cannify2 = Cannify(contimage)
        contours = cannify2.filter_contours_by_height(contours, cannify2.low_height, cannify2.high_height)

        # sort by x
        contours = sorted(contours, key=self.sort_by_x)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            digits.append(self.img[y:y+h, x:x+w])

        return digits

    @staticmethod
    def sort_by_x(c):
        x, y, w, h = cv2.boundingRect(c)
        return x

    def isolate_by_contours(self, contours):
        to_delete = []
        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            b1 = [x, y, x+w, y+h]
            for ni, n in enumerate(contours[i:]):
                nx, ny, nw, nh = cv2.boundingRect(n)
                b2 = [nx, ny, nx+nw, ny+nh]
                intersecting = len(self.intersection(b1, b2))
                if intersecting:
                    to_delete.append(ni)

        c2 = []
        for i, c in enumerate(contours):
            if i not in to_delete:
                c2.append(c)

        print('after isolate', len(contours), len(c2))
        return c2

    def union(self, a, b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0] + a[2], b[0] + b[2]) - x
        h = max(a[1] + a[3], b[1] + b[3]) - y
        return x, y, w, h

    def intersection(self, a, b):
        x = max(a[0], b[0])
        y = max(a[1], b[1])
        w = min(a[0] + a[2], b[0] + b[2]) - x
        h = min(a[1] + a[3], b[1] + b[3]) - y
        if w < 0 or h < 0: return ()  # or (0,0,0,0) ?
        return x, y, w, h
