
class ImageProcessor:

    def __init__(self, img):
        self.img = img
        self.height, self.width = self.img.shape

    def process(self):
        """ Do processing here and return the result"""
        return self.img