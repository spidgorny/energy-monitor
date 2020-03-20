import cv2
from .ImageProcessor import ImageProcessor
import random
import numpy as np
import math


class Cannify(ImageProcessor):

    def __init__(self, img, debug: bool = False):
        super().__init__(img)
        self.low_area = 300
        self.high_area = 1100
        self.low_height = 45
        self.high_height = 60
        self.digits = []
        self.debug = debug

    def process(self):
        cv2.imwrite('5-cannify.png', self.img)
        contours, hierarchy = cv2.findContours(self.img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        print('len contours', len(contours))

        contimage = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.drawContours(contimage, contours, contourIdx=-1, color=(50, 50, 50))
        if self.debug:
            cv2.imwrite('6-contours.png', contimage)

        # contours1 = self.filter_contours_by_area(contours, self.low_area, self.high_area)
        # print('len contours1', len(contours1))
        # cv2.drawContours(contimage, contours1, contourIdx=-1, color=(255, 255, 0))

        contours2 = self.filter_contours_by_height(contours, self.low_height, self.high_height)
        print('len contours2', len(contours2))
        cv2.drawContours(contimage, contours2, contourIdx=-1, color=(0, 255, 0))

        contours3 = self.filter_contours_by_aspect(contours2, 0.5, 4.e-1)
        print('len contours3', len(contours3))
        cv2.drawContours(contimage, contours3, contourIdx=-1, color=(0, 0, 255))

        average_y, average_height = self.get_average_height(contours3)
        if average_height is not None and average_height > 0:
            average_height *= 0.5
            print('average_y', average_y)
            print('average_height', average_height)
            if average_y and average_height:
                cv2.line(contimage, (0, math.floor(average_y - 0)),
                         (self.width, math.floor(average_y - 0)), color=(255, 0, 0))
                cv2.line(contimage, (0, math.floor(average_y - average_height)),
                         (self.width, math.floor(average_y - average_height)), color=(0, 0, 255))
                cv2.line(contimage, (0, math.floor(average_y + average_height)),
                         (self.width, math.floor(average_y + average_height)), color=(0, 0, 255))
                contours4 = self.filter_contours_by_position(contours3, average_y, average_height)
                print('len contours4', len(contours4))
                cv2.drawContours(contimage, contours4, contourIdx=-1, color=(0, 255, 255))

                contours5 = self.reintroduce_inner_elements(contours4, contours)
                cv2.drawContours(contimage, contours5, contourIdx=-1, color=(255, 0, 255))

                self.digits = contours5

        return contimage

    def click(self):
        # self.low_height += 5
        print(self.low_area, 'area', self.high_area)
        print(self.low_height, 'height', self.high_height)

    def filter_contours_by_area(self, contours, min_area, max_area):
        good = []
        for c in contours:
            area = cv2.contourArea(c)
            if min_area <= area <= max_area:
                good.append(c)

        return good

    def filter_contours_by_height(self, contours, min_height, max_height):
        good = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if min_height <= h <= max_height:
                # print('h', h)
                good.append(c)

        return good

    def filter_contours_by_aspect(self, contours, desired_aspect, sigma):
        good = []
        aspect_list = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w) / h
            # print('a', aspect_ratio)
            aspect_list.append(aspect_ratio)
            if np.isclose(aspect_ratio, desired_aspect, sigma):
                good.append(c)

        print('average aspect', self.mean(aspect_list))
        return good

    def mean(self, numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

    def get_average_height(self, contours):
        y_list = []
        height_list = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            y_list.append(y)
            height_list.append(h)

        average_y = None
        average_height = None
        # average_y = self.mean(y_list)
        if len(y_list):
            average_y = max(y_list, key=y_list.count)
            average_height = self.mean(height_list)
        return average_y, average_height

    def filter_contours_by_position(self, contours, average_y, average_height):
        good = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            ok = (average_y - average_height) <= y <= (average_y + average_height)
            # print((average_y - average_height), y, (average_y + average_height), ok)
            if ok:
                good.append(c)

        return good

    def reintroduce_inner_elements(self, contours_big, contours_all):
        small = []
        for n in contours_big:
            nx, ny, nw, nh = cv2.boundingRect(n)
            for c in contours_all:
                x, y, w, h = cv2.boundingRect(c)
                if w <= nw and h <= nh and x >= nx and y >= ny and x <= (nx + nw) and y <= (ny + nh):
                    small.append(c)

        print('small', len(small))
        return contours_big + small

    def getDigits(self):
        hashes = []
        unique = []
        for c in self.digits:
            h = hash(c.tobytes())
            if h not in hashes:
                hashes.append(h)
                unique.append(c)

        print('unique', len(self.digits), len(unique))
        return unique
