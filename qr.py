import cv2 as cv
import numpy as np

class QrHandler():
    def detect(self, img):
        for y in range(0, len(img)):
            for x in range(0, len(img[0])):
                if (img[y, x] < [50, 50, 50]).all():
                    print('black')

qr_handler = QrHandler()
qr_handler.detect(None)