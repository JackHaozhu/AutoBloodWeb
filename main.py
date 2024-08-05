import functions.FindGameDir
import functions.TemplateMatching
import functions.overlaying.TargetOverlay

import time
import json
import cv2
import numpy as np
import pyautogui as pag

pag.FAILSAFE = False


def read_config():
    with open(r'.\functions\config.json', 'r') as conf:
        return json.load(conf)


def write_config(config):
    with open(r'.\functions\config.json', 'w') as conf:
        json.dump(config, conf, indent=4)


def read_dict():
    with open(r'.\functions\dict.json', 'r') as dir_dic:
        return json.load(dir_dic)


def wrtie_dict(dir_dictionary):
    with open(r'.\functions\dict.json', 'w') as dir_dic:
        json.dump(dir_dictionary, dir_dic, indent=4)


def pil2opencv(pil_image):
    numpy_image = np.array(pil_image)
    cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return cv2_image


def get_template_images(category: str, name: str = 'Human'):
    config = read_config()
    targets = config[category][name]
    dir_dict = read_dict()
    template_images = []

    for target in targets:
        for item_type in dir_dict:
            for rarity in dir_dict[item_type]:
                if target in dir_dict[item_type][rarity]:
                    target_dir = dir_dict[item_type][rarity][target]
                    target_full_dir = (config['game_dir'] +
                                       '\\DeadByDaylight\\Content\\UI\\Icons\\'
                                       + item_type + target_dir + '.png')
                    background_path = '.\\functions\\overlaying\\background\\' + item_type + '\\' + rarity + '.png'
                    # print('Target Directory: ', target_full_dir)
                    # print('Background Path: ', background_path)
                    overlaid_image = functions.overlaying.TargetOverlay.overlay(background_path, target_full_dir)
                    template_images.append(pil2opencv(overlaid_image))
    return template_images


def remove_close_matches(tuples, threshold: float = 5):
    tuples = np.array(tuples, dtype=np.float64)

    keep = np.ones(len(tuples), dtype=bool)

    for i in range(len(tuples)):
        if keep[i]:
            distances = np.linalg.norm(tuples[i] - tuples[(i + 1):], axis=1)

            keep[(i + 1):] &= distances >= threshold

    return np.array(tuples[keep], dtype=np.int32)


def custom_click():
    pag.mouseDown()
    time.sleep(0.1)
    pag.mouseUp()


def group_targets(targets):
    center = np.array((1360, 1145), dtype=np.float64)
    targets = np.array(targets, dtype=np.float64)

    # group = np.ones(len(targets), dtype=int)
    grouped_targets = [[], [], []]

    for target in targets:
        distance = np.linalg.norm(target - center)

        if distance > 600:
            grouped_targets[0].append(target)
        elif distance > 400:
            grouped_targets[1].append(target)
        elif distance > 200:
            grouped_targets[2].append(target)

    return grouped_targets


def click_targets(target_positions, method: int = 0):
    if method == 0:
        for target in target_positions:
            x, y = target
            pag.moveTo(x, y)
            custom_click()
            pag.moveTo(0, 0)
            time.sleep(2)
    if method == 1:
        grouped_targets = group_targets(target_positions)
        for group in grouped_targets:
            for target in group:
                x, y = target
                pag.moveTo(x, y)
                custom_click()
                pag.moveTo(0, 0)
                time.sleep(2)

    pag.moveTo(1360, 1145)
    custom_click()
    pag.moveTo(0, 0)
    time.sleep(7)


def test_function():
    config = read_config()
    dir_dict = read_dict()

    if config['game_dir'] == '':
        config['game_dir'] = functions.FindGameDir.get_game_dir()
        write_config(config)

    templates = get_template_images('0')

    pag.moveTo(0, 0)
    screenshot = pag.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    matches = functions.TemplateMatching.match_template(templates, screenshot)
    # print(matches)
    matches = remove_close_matches(matches)
    # print(matches)
    click_targets(matches, 1)


def out_of_bloodpoints(current_image, cache_image, threshold=0.9):
    gray_current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    gray_cache_image = cv2.cvtColor(cache_image, cv2.COLOR_BGR2GRAY)

    print("Calculating Hist")
    current_hist = cv2.calcHist([gray_current_image], [0], None, [256], [0, 256])
    cach_hist = cv2.calcHist([gray_cache_image], [0], None, [256], [0, 256])

    print("Hist Normalizing")
    cv2.normalize(current_hist, current_hist)
    cv2.normalize(cach_hist, cach_hist)

    print("Starting Comparing")
    simularity = cv2.compareHist(current_hist, cach_hist, cv2.HISTCMP_CORREL)

    return simularity >= threshold


if __name__ == '__main__':
    cache = None
    count = 0
    while True:
        count += 1
        screenshot = cv2.cvtColor(np.array(pag.screenshot()), cv2.COLOR_RGB2BGR)
        if cache is not None and out_of_bloodpoints(screenshot, cache):
            print("Out of Bloodpoints!")
            break
        cache = screenshot
        test_function()
        print(f"Finished Page {count}!")
