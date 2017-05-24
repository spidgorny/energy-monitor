import random
from ppretty import ppretty
import numpy as np
import matplotlib.pyplot as plt
import cv2
from os import path, listdir
from beeprint import pp
import yaml


class Train:
    def __init__(self):
        self.mypath = 'training/'
        self.onlyfiles = [f for f in listdir(self.mypath)
                          if path.isfile(path.join(self.mypath, f))]
        self.file = None

    def train(self):
        all_digits = np.zeros((0, 450), dtype=np.float32)
        all_numbers = np.zeros(0, dtype=np.float32)
        for file in self.onlyfiles:
            self.file = path.join(self.mypath, file)
            print(self.file)
            digits, numbers = self.read_file(self.file)
            # print(len(digits), len(numbers))

            digits = self.reshape_digits(digits)

            for d in digits:
                print(all_digits.shape, d.shape)
                all_digits = np.append(all_digits, [d], 0)

            numbers = self.reshape_numbers(numbers)
            all_numbers = np.append(all_numbers, numbers, 0)

        print('all_digits', all_digits.shape, all_digits.dtype)
        print('all_numbers', all_numbers.shape, all_numbers.dtype)

        knn = cv2.ml.KNearest_create()
        knn.train(all_digits, cv2.ml.ROW_SAMPLE, all_numbers)

        check = np.asarray([all_digits[0]])
        ret, results, neighbours, dist = knn.findNearest(check, 5)
        print('check', check.shape, results[0])
        # [0, 4, 6, 3, 0, 8]
        # pp([ret, results, neighbours, dist])

        check = np.asarray([all_digits[1]])
        ret, results, neighbours, dist = knn.findNearest(check, 5)
        print('check', check.shape, results[0])
        # [0, 4, 6, 3, 0, 8]
        # pp([ret, results, neighbours, dist])

    def read_file(self, filename):
        fs = cv2.FileStorage(filename, flags=0)

        digit_list = []
        i = 0
        while True:
            key = "digit" + str(i)
            data = fs.getNode(key)
            if data.mat() is None:
                break
            else:
                # print(key, data.mat())
                digit_list.append(data.mat())
            i += 1

        numbers = fs.getNode('numbers')
        num_list = []
        for i in range(0, numbers.size()):
            num_list.append(numbers.at(i).real())

        # print(num_list)
        fs.release()
        return digit_list, num_list

    def reshape_digits(self, digits):
        # reshape
        for i, d in enumerate(digits):
            d = cv2.resize(d, (30, 15))
            d = np.reshape(d, 30 * 15)
            d = d.astype(np.float32)
            digits[i] = d

        # digits = np.asanyarray(digits) #, dtype=np.uint8)
        digits = np.stack(digits)
        # print('digits', digits.shape)
        return digits

    def reshape_numbers(self, numbers):
        numbers = np.asarray(numbers)
        numbers = numbers.astype(np.float32)
        # print('numbers', numbers.shape)
        return numbers


t = Train()
t.train()
