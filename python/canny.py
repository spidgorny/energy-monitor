import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import pi


class Canny:

    def __init__(self):
        self.img = cv2.imread('../cache/20170516-001058.png', 0)

    def render(self):
        lines = cv2.HoughLines(self.img, 1, pi / 180, 140, min_theta=60 * pi / 180, max_theta=120 * pi / 180)
        #print(lines)
        skew = self.detect_skew(lines)
        print("detectSkew: %.1f deg", skew)

        straight = self.rotate(self.img, -skew)

        edges = cv2.Canny(straight, 100, 200)

        plt.subplot(221)
        plt.imshow(self.img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(222), plt.imshow(straight, cmap='gray')
        plt.title('Straight Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(223), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show()

    def filter_lines(self, lines):
        theta_min = 60 * pi / 180
        theta_max = 120 * pi / 180
        theta_avr = 0
        theta_deg = 0
        # for i = 0; i < lines.size(); i++:
        #     float theta = lines[i][1];
        #     if (theta >= theta_min && theta <= theta_max) {
        #         filteredLines.push_back(lines[i]);
        #         theta_avr += theta;
        #     }
        # }

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


x = Canny()
x.render()
