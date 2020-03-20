import configparser

import cv2
from os import path

import numpy as np

from Image.Cannify import Cannify
from Image.IsolateDigits import IsolateDigits
from Image.Straighten import Straighten
from config import config_ocr


class Pipeline:

    def __init__(self, filename: str):
        self.file = filename
        self.img = cv2.imread(self.file, 0)
        self.height, self.width = self.img.shape
        """ :var Canny """
        self.cannify = None
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.config: map = config['Pipeline']
        self.debug: bool = bool(self.config['debug'])

    def process(self):
        if self.debug:
            cv2.imwrite('1-original.png', self.img)

        edges = cv2.Canny(self.img,
                          int(self.config['canny.threshold1']),
                          int(self.config['canny.threshold2']))
        if self.debug:
            cv2.imwrite('2-edges.png', edges)

        straighten = Straighten(edges, debug=self.debug)
        straight = straighten.process()
        if self.debug:
            cv2.imwrite('4-straight.png', straight)

        self.cannify = Cannify(straight, debug=self.debug)
        contimage = self.cannify.process()
        contours = self.cannify.getDigits()

        isolated = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.drawContours(isolated, contours, contourIdx=-1, color=(255, 255, 255))
        # thickness=cv2.FILLED)
        if self.debug:
            cv2.imwrite('7-isolated.png', isolated)

        # alternatively fill the contours
        # todo: this does not let openings
        # for c in contours:
        #     cv2.fillPoly(isolated, pts=[c], color=(255, 255, 255))

        isolator = IsolateDigits(isolated)
        digits = isolator.isolate(contours)

        return straight, edges, contimage, isolated, digits

    def resizeReshape(self, digits):
        # resize, reshape
        dimentions = config_ocr['sample_size'][0] * config_ocr['sample_size'][1]
        samples = np.zeros((0, dimentions))
        for d in digits:
            d30 = cv2.resize(d, config_ocr['sample_size'], interpolation=cv2.INTER_LANCZOS4)
            gray = cv2.cvtColor(d30, cv2.COLOR_BGR2GRAY)
            features = np.reshape(gray, dimentions)
            samples = np.append(samples, [features], 0)

        return samples
