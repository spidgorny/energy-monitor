# import random
# from ppretty import ppretty
import numpy
import numpy as np
# import matplotlib.pyplot as plt
import cv2
from os import path, listdir
# from beeprint import pp
# import yaml
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import pickle
import os
from sklearn.naive_bayes import GaussianNB
from config import config_ocr


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

        knn = False
        svm = False
        svc = False
        gnb = False
        snn = True
        # knn = cv2.ml.KNearest_create()
        if knn:
            knn.train(self.all_digits, cv2.ml.ROW_SAMPLE, self.all_numbers)
            self.check_one_digit(knn)
            self.check_all_digits(knn)
            self.check_split_digits()
            knn.save('ocr.knn')
        elif svm:
            # unfinished since there is no load() method
            svm = cv2.ml.SVM_create()
            svm.train(self.all_digits, cv2.ml.ROW_SAMPLE, self.all_numbers)
        elif svc:
            self.test_svc()
        elif gnb:
            self.test_gnb()
        elif snn:
            self.test_snn()
        else:
            raise RuntimeError('Unspecified classifier')

    def test_snn(self):
        self.all_digits, self.all_numbers = self.removeInf()
        X_trn, X_tst, y_trn, y_tst = train_test_split(self.all_digits, self.all_numbers, test_size=0.2)
        clf = KNeighborsClassifier()
        clf.fit(X_trn, y_trn)
        pred = clf.predict(X_tst)
        acc = accuracy_score(pred, y_tst)
        print('accuracy', '{:.2f}'.format(acc * 100.0), '%')

        print(list(range(10)))
        numpy.set_printoptions(threshold=numpy.nan)
        print(metrics.confusion_matrix(y_tst, pred, range(10)))

        with open('ocr.snn', 'wb') as pickle_file:
            pickle.dump(clf, pickle_file)

        statinfo = os.stat('ocr.snn')
        print('size', statinfo.st_size)

    def test_gnb(self):
        self.all_digits, self.all_numbers = self.removeInf()
        X_trn, X_tst, y_trn, y_tst = train_test_split(self.all_digits, self.all_numbers, test_size=0.2)
        clf = GaussianNB()
        clf.fit(X_trn, y_trn)
        pred = clf.predict(X_tst)
        acc = accuracy_score(pred, y_tst)
        print('accuracy', '{:.2f}'.format(acc * 100.0), '%')

        with open('ocr.gnb', 'wb') as pickle_file:
            pickle.dump(clf, pickle_file)

        statinfo = os.stat('ocr.gnb')
        print('size', statinfo.st_size)

    def test_svc(self):
        self.all_digits, self.all_numbers = self.removeInf()
        X_trn, X_tst, y_trn, y_tst = train_test_split(self.all_digits, self.all_numbers, test_size=0.2)
        clf = SVC()
        clf.fit(X_trn, y_trn)
        pred = clf.predict(X_tst)
        acc = accuracy_score(pred, y_tst)
        print('accuracy', '{:.2f}'.format(acc * 100.0), '%')

        with open('ocr.svm', 'wb') as pickle_file:
            pickle.dump(clf, pickle_file)

        statinfo = os.stat('ocr.svm')
        print('size', statinfo.st_size)

    def removeInf(self):
        to_delete = []
        for i, n in enumerate(self.all_numbers):
            if n == np.Inf:
                to_delete.append(i)

        a = np.delete(self.all_digits, to_delete, axis=0)
        b = np.delete(self.all_numbers, to_delete, axis=0)
        print('to_delete', len(to_delete))
        print('removeInf', self.all_digits.shape, self.all_numbers.shape)
        print('removeInf', a.shape, b.shape)
        return a, b

    def check_split_digits(self):
        X_trn, X_tst, y_trn, y_tst = train_test_split(self.all_digits, self.all_numbers, test_size=0.2)

        knn = cv2.ml.KNearest_create()
        knn.train(X_trn, cv2.ml.ROW_SAMPLE, y_trn)

        ret, results, neighbours, dist = knn.findNearest(X_tst, 5)
        results = np.reshape(results, (len(results)))
        print(y_tst.shape, results.shape)

        # replace inf @see if we should remove them at all
        y_tst[y_tst == np.Inf] = 9999

        # print(y_tst)
        # print(results)
        accuracy = accuracy_score(y_tst, results)
        print('accuracy', '{:.2f}'.format(accuracy * 100.0), '%')

    def check_all_digits(self, knn):
        ret, results, neighbours, dist = knn.findNearest(self.all_digits, 5)
        results = np.reshape(results, (len(results)))
        print(len(results), results.shape)
        print(len(self.all_numbers), self.all_numbers.shape)
        the_same = results == self.all_numbers
        correct = np.count_nonzero(the_same)
        # print(the_same)
        p_correct = correct * 100.0 / self.all_digits.shape[0]
        print(len(the_same), correct, self.all_digits.shape[0], '{:.2f}'.format(p_correct), '%')

    def check_one_digit(self, knn):
        check = np.asarray([self.all_digits[0]])
        ret, results, neighbours, dist = knn.findNearest(check, 5)
        # pp([ret, results, neighbours, dist])
        print('check', check.shape, results[0])
        # [0, 4, 6, 3, 0, 8]
        print(results[0], self.all_numbers[0])
        assert(results[0] == self.all_numbers[0])

    def read_files(self):
        dimentions = config_ocr['sample_size'][0] * config_ocr['sample_size'][1]
        all_digits = np.zeros((0, dimentions), dtype=np.float32)
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
            d = cv2.resize(d, config_ocr['sample_size'])
            d = np.reshape(d, config_ocr['sample_size'][0] * config_ocr['sample_size'][1])
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

