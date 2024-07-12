import cv2
import numpy as np


def match_template(template_images, main_image):
    center_points = []
    w, h = 47, 47
    for n,template in enumerate(template_images):
        result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

        treshold = 0.8
        loc = np.where(result >= treshold)

        for pt in zip(*loc[::-1]):
            center_x = pt[0] + 47
            center_y = pt[1] + 47
            center_points.append((center_x, center_y))

    return center_points


if __name__ == '__main__':
    ...
