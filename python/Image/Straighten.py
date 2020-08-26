import math

import cv2
from .ImageProcessor import ImageProcessor
from math import pi
import configparser


class Straighten(ImageProcessor):

    def __init__(self, img, debug: bool = False):
        super().__init__(img)
        """

        @type debug: bool
        """
        self.debug = debug
        print('debug', self.debug)

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def process(self):
        print('HoughLines...')
        cThreshold = int(self.config['Straighten']['threshold'])
        print('cThreshold', cThreshold)
        #                                pixel  degree=1        min lines
        lines = cv2.HoughLines(self.img, rho=1, theta=pi / 180,
                               threshold=cThreshold, lines=60 * pi / 180, srn=120 * pi / 180)
        print(len(lines), 'lines')

        if self.debug:
            imageWithLines = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
            for line in lines:
                rho = line[0][0]
                theta = line[0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))

                # https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
                cv2.line(imageWithLines, pt1, pt2, (255, 0, 0))
            cv2.imwrite('3-lines.png', imageWithLines)

        # print(lines)
        if lines is not None:
            skew = self.detect_skew(lines)
            print("detectSkew: %.1f deg", skew)

            straight = self.rotate(self.img, -skew)
            return straight
        else:
            return self.img

    def detect_skew(self, lines):
        theta_avr = 0
        for line in lines:
            # print(line)
            theta_avr += line[0][1]

        theta_deg = 0
        if len(lines):
            theta_avr /= len(lines)
            theta_deg = (theta_avr / pi * 180) - 90

        return theta_deg

    def rotate(self, img, skew):
        height, width = img.shape
        M = cv2.getRotationMatrix2D((width / 2, height / 2), skew * 2, 1)
        img_rotated = cv2.warpAffine(img, M, img.shape[::-1])
        return img_rotated
