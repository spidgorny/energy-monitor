import os.path as path
from os import listdir
import cv2
from matplotlib import pyplot as plt
from Image.IsolateDigits import IsolateDigits
from Image.Straighten import *
from Image.Cannify import *
# from matplotlib.widgets import Button
import multiprocessing


class Canny:

    def __init__(self):
        print('Reading files...')
        self.mypath = '../cache/'
        self.onlyfiles = [f for f in listdir(self.mypath)
                     if path.isfile(path.join(self.mypath, f))]
        self.file = None
        self.img = None
        self.width = None
        self.height = None
        self.cannify = None

    def next_image(self):
        self.file = random.choice(self.onlyfiles)
        print('file', self.file)

        self.img = cv2.imread(path.join(self.mypath, self.file), 0)
        self.height, self.width = self.img.shape

        self.render()

    def render(self):
        straighten = Straighten(self.img)
        straight = straighten.process()

        edges = cv2.Canny(straight, 100, 200)

        self.cannify = Cannify(edges)
        contimage = self.cannify.process()
        contours = self.cannify.getDigits()

        isolated = np.zeros((self.height, self.width, 3), np.uint8)
        # cv2.drawContours(isolated, contours, contourIdx=-1, color=(255, 255, 255), thickness=cv2.FILLED)
        for c in contours:
            cv2.fillPoly(isolated, pts=[c], color=(255, 255, 255))

        isolator = IsolateDigits(isolated)
        digits = isolator.isolate(contours)

        digimage = np.zeros((self.height, self.width, 3), np.uint8)
        # normalized_contours = self.normalize_contours(contours)
        # cv2.drawContours(digimage, normalized_contours, contourIdx=-1, color=(200, 200, 200))
        for i, d in enumerate(digits):
            d25 = cv2.resize(d, (15, 30), interpolation=cv2.INTER_LANCZOS4)
            self.OverlayImage(digimage, d25, i * 40, 0, (0, 0, 0, 0), (1, 1, 1, 1))

        # self.plot(straight, edges, contimage, isolated, digimage)
        # job_for_another_core = multiprocessing.Process(target=self.plot,
        #                                                args=(straight, edges, contimage, isolated, digimage))

        job_for_another_core = multiprocessing.Process(target=self.plot_result,
                                                       args=[digimage])
        job_for_another_core.start()

        numbers = ''
        while len(numbers) != len(digits):
            numbers = input('Numbers [x' + str(len(digits)) + ']:')
            print(numbers)

        job_for_another_core.terminate()
        self.saveDigits(digits, list(numbers))  # list of digits, not a whole number

    def plot(self, straight, edges, contimage, isolated, digimage):
        plt.subplot(231), plt.imshow(self.img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(232), plt.imshow(straight, cmap='gray')
        plt.title('Straight Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(233), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(234), plt.imshow(contimage)
        plt.title('Contours'), plt.xticks([]), plt.yticks([])

        plt.subplot(235), plt.imshow(isolated, cmap='gray')
        plt.title('Isolated'), plt.xticks([]), plt.yticks([])

        plt.subplot(236), plt.imshow(digimage, cmap='gray')
        plt.title('Digits'), plt.xticks([]), plt.yticks([])

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0.01)

        if False:
            mng = plt.get_current_fig_manager()
            if "state" in dir(mng.window):
                mng.window.state('zoomed')
            elif "frame" in dir(mng):
                mng.frame.Maximize(True)
            else:
                mng.window.showMaximized()

        # fig = plt.figure()
        # mng.canvas.mpl_connect('button_press_event', self.onclick)

        # bnext = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Next')
        # bnext.on_clicked(self.next_image)
        # plt.ion()
        plt.ioff()

        figure = plt.gcf()
        dpi = figure.get_dpi()
        # print('dpi', dpi)
        figure.set_size_inches((640*3/dpi, 480*2/dpi), forward=True)
        # plt.rcParams["figure.figsize"] = (50, 30)
        plt.show()

    def plot_result(self, digimage):
        plt.imshow(digimage, cmap='gray')
        plt.title('Digits'), plt.xticks([]), plt.yticks([])

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0.01)
        figure = plt.gcf()
        dpi = figure.get_dpi()
        # print('dpi', dpi)
        figure.set_size_inches((640 / dpi, 480 / dpi), forward=True)
        plt.show()

    def onclick(self, event):
        print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  (event.button, event.x, event.y, event.xdata, event.ydata))
        self.cannify.click()
        contimage = self.cannify.process()
        plt.subplot(224), plt.imshow(contimage)
        event.canvas.draw()

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

    def normalize_contours(self, contours):
        print('before normalize', len(contours))
        # cv2.drawContours(digimage, contours, contourIdx=-1, color=(50, 50, 50))

        normalized_contours = []
        for cn, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            c2 = np.zeros(c.shape, c.dtype)
            print('c', c.shape, c.dtype, len(c))
            for i, coord_list in enumerate(c):
                coord = coord_list[0]
                # print('coord', coord)
                # print(i, 'c2', c2, coord[0, 0], x)
                # c2.itemset((i, 0, 0), coord[0, 0]-x)
                # c2.itemset((i, 0, 1), coord[0, 1]-y)
                c2[i, 0, 0] = coord[0] - x + 25 * cn
                c2[i, 0, 1] = coord[1] - y

            print('c2', c2.shape, c2.dtype, len(c2))
            # cv2.drawContours(digimage, c2, contourIdx=-1, color=(200, 200, 200))
            normalized_contours.append(c2)

        print('after normalize', len(normalized_contours))
        return normalized_contours

    def OverlayImage(self, src, overlay, posx, posy, S, D):
        o_height, o_width, _ = overlay.shape
        s_height, s_width, _ = src.shape
        for x in range(o_width):
            if x+posx < s_width:
                for y in range(o_height):
                    if y+posy < s_width:

                        source = src[y+posy, x+posx]
                        over = overlay[y, x]
                        merger = [0, 0, 0, 0]

                        for i in range(1):
                            merger[i] = (S[i]*source[i]+D[i]*over[i])

                        # merged = tuple(merger)
                        src[y+posy, x+posx] = merger[0]

    def saveDigits(self, digits, numbers):
        filename = path.basename(self.file)
        filename = filename.replace('.png', '.yml')
        fs = cv2.FileStorage(path.join("training/", filename), flags=1)

        for i, d in enumerate(digits):
            gray = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
            fs.write("digit" + str(i), gray)

        # numbers = np.asarray(numbers, dtype=np.uint8)
        # fs.write("numbers", numbers)
        fs.release()

        with open(path.join("training/", filename), "a") as myfile:
            myfile.write("numbers: [" + ', '.join(numbers) + "]\n")
        print('done')

