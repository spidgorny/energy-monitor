import configparser
import cv2
import numpy as np
from Image.Cannify import Cannify
from Image.IsolateDigits import IsolateDigits
from Image.Straighten import Straighten


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
        self.sample_size = eval(self.config['sample_size'])
        print('sample_size', type(self.sample_size), self.sample_size)

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
        """
        Reformat from 2D image with 3 color channels
        to a single line of pixels for machine learning
        (actually x*y features of a single pixel)
        @param digits:
        @return:
        """
        print('original shape', len(digits), digits[0].shape)
        dimentions = self.sample_size[0] * self.sample_size[1]
        samples = np.zeros((0, dimentions))
        for d in digits:
            d30 = cv2.resize(d, self.sample_size, interpolation=cv2.INTER_LANCZOS4)
            gray = cv2.cvtColor(d30, cv2.COLOR_BGR2GRAY)
            features = np.reshape(gray, dimentions)
            samples = np.append(samples, [features], 0)

        print('resulting shape', len(samples), samples[0].shape)
        return samples
