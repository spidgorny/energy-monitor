import os.path as path
from os import listdir
import cv2
from matplotlib import pyplot as plt
from Image.Straighten import *
from Image.Cannify import *
from matplotlib.widgets import Button


class Canny:

    def __init__(self):
        self.mypath = '../cache/'
        self.onlyfiles = [f for f in listdir(self.mypath)
                     if path.isfile(path.join(self.mypath, f))]
        self.img = None
        self.width = None
        self.height = None
        self.next_image()

    def next_image(self):
        file = random.choice(self.onlyfiles)
        print('file', file)

        self.img = cv2.imread(path.join(self.mypath, file), 0)
        self.height, self.width = self.img.shape

        self.render()

    def render(self):
        straighten = Straighten(self.img)
        straight = straighten.process()

        edges = cv2.Canny(straight, 100, 200)

        self.cannify = Cannify(edges)
        contimage = self.cannify.process()

        plt.subplot(221), plt.imshow(self.img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(222), plt.imshow(straight, cmap='gray')
        plt.title('Straight Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(223), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(224), plt.imshow(contimage)
        plt.title('Contours'), plt.xticks([]), plt.yticks([])

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0.01)
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


x = Canny()
while True:
    x.next_image()
