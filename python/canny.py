import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import pi
from os import listdir
import os.path as path
import random


class Canny:

    def __init__(self):
        mypath = '../cache/'
        onlyfiles = [f for f in listdir(mypath)
                     if path.isfile(path.join(mypath, f))]
        file = random.choice(onlyfiles)

        self.img = cv2.imread(path.join(mypath, file), 0)
        self.height, self.width = self.img.shape

    def render(self):
        lines = cv2.HoughLines(self.img, 1, pi / 180, 140, min_theta=60 * pi / 180, max_theta=120 * pi / 180)
        #print(lines)
        skew = self.detect_skew(lines)
        print("detectSkew: %.1f deg", skew)

        straight = self.rotate(self.img, -skew)

        edges = cv2.Canny(straight, 100, 110)

        contimage, contours, hierarchy = cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

        contimage = np.zeros((self.height, self.width, 3), np.uint8)
        contours = self.filter_contours(contours, 100, 1000)
        cv2.drawContours(contimage, contours, contourIdx=-1, color=(255, 255, 0))

        c_good_aspect = []
        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w) / h
            if np.isclose(aspect_ratio, 0.5, 1.e-1):
                c_good_aspect.append(c)
                cv2.drawContours(contimage, c_good_aspect, contourIdx=len(c_good_aspect)-1, color=(255, 0, 0))
            else:
                cv2.drawContours(contimage, contours, contourIdx=i, color=(random.random()*255,
                                                                           random.random()*255,
                                                                           random.random()*255))

        plt.subplot(221), plt.imshow(self.img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(222), plt.imshow(straight, cmap='gray')
        plt.title('Straight Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(223), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(224), plt.imshow(contimage, cmap='gray')
        plt.title('Contours'), plt.xticks([]), plt.yticks([])

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        mng = plt.get_current_fig_manager()
        # mng.frame.Maximize(True)
        mng.window.state('zoomed')

        def onclick(event):
            print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  (event.button, event.x, event.y, event.xdata, event.ydata))

        # fig = plt.figure()
        mng.canvas.mpl_connect('button_press_event', onclick)
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

    def filter_contours(self, contours, min_area, max_area):
        good = []
        print('len conours', len(contours))
        for c in contours:
            area = cv2.contourArea(c)
            if min_area <= area <= max_area:
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = float(w) / h
                print(x, y, w, h, aspect_ratio)
                good.append(c)

        return good


x = Canny()
x.render()
