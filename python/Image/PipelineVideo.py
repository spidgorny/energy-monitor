import cv2

from Image.Pipeline import Pipeline


class PipelineVideo(Pipeline):

    def __init__(self, frame):
        self.img = frame
        self.height, self.width = self.img.shape
        """ :var Canny """
        self.cannify = None