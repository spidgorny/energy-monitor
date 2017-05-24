import random
from ppretty import ppretty
import numpy as np
import matplotlib.pyplot as plt
import cv2
from os import path, listdir
from beeprint import pp
import yaml
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class Train:
    def __init__(self):
        self.mypath = 'training/'
        self.onlyfiles = [f for f in listdir(self.mypath)
                          if path.isfile(path.join(self.mypath, f))]
        self.file = None
        self.all_digits = None
        self.all_numbers = None

    def train(self):
        self.all_digits, self.all_numbers = self.read_files()
        print('all_digits', self.all_digits.shape, self.all_digits.dtype)
        print('all_numbers', self.all_numbers.shape, self.all_numbers.dtype)

        knn = cv2.ml.KNearest_create()
        knn.train(self.all_digits, cv2.ml.ROW_SAMPLE, self.all_numbers)

        self.check_one_digit(knn)
        self.check_all_digits(knn)
        self.check_split_digits()

    def check_split_digits(self):
        X_trn, X_tst, y_trn, y_tst = train_test_split(self.all_digits, self.all_numbers, test_size=0.2)

        knn = cv2.ml.KNearest_create()
        knn.train(X_trn, cv2.ml.ROW_SAMPLE, y_trn)

        ret, results, neighbours, dist = knn.findNearest(X_tst, 5)
        results = np.reshape(results, (len(results)))
        print(y_tst.shape, results.shape)
        accuracy = accuracy_score(y_tst, results)
        print('accuracy', accuracy * 100.0, '%')

    def check_all_digits(self, knn):
        ret, results, neighbours, dist = knn.findNearest(self.all_digits, 5)
        results = np.reshape(results, (len(results)))
        print(len(results), results.shape)
        print(len(self.all_numbers), self.all_numbers.shape)
        the_same = results == self.all_numbers
        correct = np.count_nonzero(the_same)
        # print(the_same)
        print(len(the_same), correct, self.all_digits.shape[0], correct * 100.0 / self.all_digits.shape[0], '%')

    def check_one_digit(self, knn):
        check = np.asarray([self.all_digits[0]])
        ret, results, neighbours, dist = knn.findNearest(check, 5)
        # pp([ret, results, neighbours, dist])
        print('check', check.shape, results[0])
        # [0, 4, 6, 3, 0, 8]
        assert(results[0] == self.all_numbers[0])

    def read_files(self):
        all_digits = np.zeros((0, 450), dtype=np.float32)
        all_numbers = np.zeros(0, dtype=np.float32)
        for file in self.onlyfiles:
            self.file = path.join(self.mypath, file)
            print(self.file)
            digits, numbers = self.read_file(self.file)
            # print(len(digits), len(numbers))

            digits = self.reshape_digits(digits)

            for d in digits:
                # print(all_digits.shape, d.shape)
                all_digits = np.append(all_digits, [d], 0)

            numbers = self.reshape_numbers(numbers)
            all_numbers = np.append(all_numbers, numbers, 0)
        return all_digits, all_numbers

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
