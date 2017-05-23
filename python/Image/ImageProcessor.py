
class ImageProcessor:

    def __init__(self, img):
        self.img = img
        # https://stackoverflow.com/questions/21483301/how-to-unpack-optional-items-from-a-tuple
        self.height, self.width, _ = (list(self.img.shape) + [None]*3)[:3]

    def process(self):
        """ Do processing here and return the result"""
        return self.img
