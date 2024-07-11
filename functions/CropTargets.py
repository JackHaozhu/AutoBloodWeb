import pyautogui, cv2
import numpy as np
import time
from PIL import Image


default_resolution = (3840, 2160)

center = (1370, 1145)
outer = [(1370, 432), (1720, 535), (1980, 800), (2060, 1145), (1980, 1490), (1720, 1755),
         (1370, 1858), (1020, 1755), (760, 1490), (680, 1145), (760, 800), (1020, 535)]
intermediate = [(1485, 710), (1690, 835), (1800, 1030), (1800, 1260), (1690, 1455), (1485, 1580),
                (1255, 1580), (1050, 1455), (940, 1260), (940, 1030), (1050, 835), (1255, 710)]
inner = [(1370, 930), (1545, 1040), (1545, 1250),
         (1370, 1360), (1195, 1250), (1195, 1040)]
all_center = [outer, intermediate, inner]


def pil2cv(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def snip_target(positions: list,extension: int = 125) -> list:
    targets = []
    screenshot = pyautogui.screenshot()
    screen_width, screen_height = pyautogui.size()
    ext = extension * screen_width // 3840

    for x,y in positions:
        crop_box = (x - ext, y - ext, x + ext, y + ext)
        img = pil2cv(screenshot.crop(crop_box))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        targets.append(img)
        # cv2.imshow('11', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return targets


def get_all():
    all_outer = snip_target(outer)
    all_intermediate = snip_target(intermediate)
    all_inner = snip_target(inner)

    return all_outer, all_intermediate, all_inner


if __name__ == '__main__':
    time.sleep(2)
    outer_targets = snip_target(outer)
    intermediate_targets = snip_target(intermediate)
    inner_targets = snip_target(inner)



