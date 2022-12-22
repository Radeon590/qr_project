import cv2 as cv
import numpy as np


class QrHandler():
    def detect(self, img):
        for y in range(0, len(img)):
            for x in range(0, len(img[0])):
                if (img[y, x] < 50).all():
                    square_length = self._get_square_length(img, y, x)
                    if square_length != -5 and self._is_has_lil_square(img, y, x, square_length):
                        qr_size = 0
                        for y_2 in range(y + square_length, len(img)):
                            if img[y_2, x] < 50:
                                square_length_2 = self._get_square_length(
                                    img, y_2, x)
                                if square_length_2 != -5 and self._is_has_lil_square(img, y_2, x, square_length_2):
                                    if square_length_2 in range(square_length - 3, square_length + 3):
                                        square_length_3 = self._get_square_length(
                                            img, y, x + qr_size)
                                        if square_length_3 != -5 and self._is_has_lil_square(img, y, x + qr_size, square_length_3):
                                            return img[y: y + qr_size + square_length, x: x + qr_size + square_length]
                            qr_size += 1

    # не забываем про помехи на изображении, поэтому при проверке какой-либо точки нужно проверять небольшой регион вокруг этой точки

    def _is_black_point(self, img, y, x, inaccuracy):
        y_2 = y + inaccuracy
        if y_2 >= len(img):
            y_2 = len(img) - 1
        x_2 = x + inaccuracy
        if x_2 >= len(img[0]):
            x_2 = len(img[0]) - 1
        for y in range(y - inaccuracy, y_2):
            for x in range(x - inaccuracy, x_2):
                if img[y, x] < 50:
                    return True

    def _get_square_length(self, img, y, x):
        square_length = 0
        # идём вправо и ищем конец квадрата, ищем его примерную длину
        for x in range(x, len(img[0])):
            if img[y, x] > 50:
                break
            square_length += 1
        # слишком маленькая длина явно говорит нам о том, что это неподходящий квадратик, поэтому проверяем
        if square_length >= 6:
            if self._is_black_point(img, y + square_length, x + square_length, 3) and self._is_black_point(img, y + square_length, x, 3):
                return square_length
        return -5

    def _is_has_lil_square(self, img, y, x, square_length):
        lil_square_length = 0
        y = y + square_length // 2
        x = x + square_length // 2
        have_white = False
        for x_lil in range(x, x + square_length):
            if img[y, x_lil] > 50:
                have_white = True
                break
            lil_square_length += 1
        if have_white:
            have_white = False
            lil_square_length_y = 0
            for y_lil in range(y, y + square_length):
                if img[y_lil, x] > 50:
                    have_white = True
                    break
                lil_square_length_y += 1
            if have_white and (lil_square_length_y in range(lil_square_length - 1, lil_square_length + 1)):
                return True
        return False


img = cv.imread('qr_code.jpg', cv.IMREAD_GRAYSCALE)
qr_handler = QrHandler()
img = qr_handler.detect(img)
cv.imshow('test', img)
cv.waitKey(0)
