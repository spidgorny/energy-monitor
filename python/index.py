from multiprocessing import freeze_support
from Recognize.Canny import Canny

if __name__ == '__main__':
    freeze_support()

    x = Canny()
    while True:
        x.next_image()
        # digimage = np.zeros((10, 10, 1), np.uint8)
        # x.saveDigits(digimage, [1, 2, 3])
