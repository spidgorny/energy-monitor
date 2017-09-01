import cv2
from .ImageProcessor import ImageProcessor
from math import pi


class Straighten(ImageProcessor):

    def process(self):
        lines = cv2.HoughLines(self.img, 1, pi / 180, 140, 60 * pi / 180, 120 * pi / 180)
        #print(lines)
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

