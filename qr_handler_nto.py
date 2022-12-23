import cv2 as cv
import numpy as np


class QR_handler():
    def _string_to_bits(self, s=''):
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def _bits_to_string(self, b=None):
        return ''.join([chr(int(x, 2)) for x in b])

    def _is_square(self, img, y, x):
        black_counter_x = 1
        for x_i in range(x + 1, len(img[0])):
            if (img[y, x_i] > [128, 128, 128]).all():
                black_counter_y = 1
                for y_i in range(y, len(img)):
                    if (img[y_i, x] > [128, 128, 128]).all():
                        if black_counter_x in range(black_counter_y - 3, black_counter_y + 3):
                            return True, black_counter_x
                        break
                    black_counter_y += 1
                break
            black_counter_x += 1
        return False, 0

    def _find_qr_bit_size(self, img):
        y = x = 0
        bit_counter = 0
        while (img[y, x] < [128, 128, 128]).all():
            bit_counter += 1
            y += 1
            x += 1
        return bit_counter

    def _check_bit(self, img, y, x):
        if (img[y, x] < [128, 128, 128]).any():
            return '1'
        return '0'

    def _xor_masked(self, bin_number, mask):
        result = ''
        if len(bin_number) != len(bin_number):
            return 'len of bin_number != len of mask'
        for i in range(0, len(bin_number)):
            if bin_number[i] == mask[i]:
                result += '0'
            else:
                result += '1'
        return result

    """def _get_symbol_length_bin(self, data_mode):
        if"""

    def _detec_qr(self, img):
        for y in range(0, len(img)):
            for x in range(0, len(img[0])):
                if (img[y, x] < [128, 128, 128]).all():
                    is_square, square_length = self._is_square(img, y, x)
                    if is_square:
                        print(square_length)
                        for x_i in range(x + square_length, len(img[0])):
                            if (img[y, x_i] < [128, 128, 128]).all():
                                is_square_2, square_length_2 = self._is_square(
                                    img, y, x_i)
                                if is_square_2 and (square_length_2 in range(square_length - 3, square_length + 3)):
                                    qr_length = x_i - x
                                    is_square_3, square_length_3 = self._is_square(
                                        img, y + qr_length, x)
                                    if is_square_3 and (square_length_3 in range(square_length - 3, square_length + 3)):
                                        return y, x, qr_length, square_length
        return -100, -100, -100, -100

    def get_qr_points(self, img):
        y, x, qr_length, square_length = self._detec_qr(img)
        if y != -100:
            return np.array([[[y, x],
                             [y + qr_length + square_length, x],
                             [y + qr_length + square_length,
                                 x + qr_length + square_length],
                             [y, x + qr_length + square_length]]])
        return None

    def get_qr_img(self, img):
        y, x, qr_length, square_length = self._detec_qr(img)
        if y != -100:
            return img[y:y + qr_length + square_length, x:x + qr_length + square_length]
        return None

    def decode_qr(self, img, square_length):
        bit_size = self._find_qr_bit_size(img)
        # determine mask mode
        mask_mode = ''
        for x in range(bit_size * 2, bit_size * 5, bit_size):
            mask_mode += self._check_bit(img, (square_length + bit_size), x)
        mask_mode = self._xor_masked(mask_mode, '101')
        print(mask_mode)
        # determine data mode
        data_mode = ''
        for y in range(len(img) - 1, len(img) - 2 - 2 * bit_size, -bit_size):
            for x in range(len(img[0]) - 1, len(img[0]) - 2 - 2 * bit_size, -bit_size):
                data_mode += self._check_bit(img, y, x)
        print('data_mode', data_mode)
        print(img[len(img) - 2 - 2 * bit_size, len(img[0]) - 2 * bit_size])
        packages_number = ''
        for y in range(len(img) - 2 - 2 * bit_size, len(img) - 2 - 8 * bit_size, - bit_size):
            for x in range(len(img[0]) - 1, len(img[0]) - 2 - 2 * bit_size, -bit_size):
                packages_number += self._check_bit(img, y, x)
        print(packages_number)
        print(self._string_to_bits('habr'))
        print(self._bits_to_string('01111001'))


img = cv.imread('qr_code.jpg', cv.IMREAD_COLOR)
handler = QR_handler()
img = handler.get_qr_img(img)
cv.imshow('test', img)
cv.waitKey(0)
