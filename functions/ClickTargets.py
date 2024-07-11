import cv2
import json
import time
import pyautogui
import CropTargets
import FindGameDir
import TemplateMatch

pyautogui.FAILSAFE = False


def read_dict():
    with open('dict.json', 'r') as f:
        data = json.load(f)
    return data


def read_config():
    with open('config.json', 'r') as config:
        data = json.load(config)
    return data


def write_config(data) -> None:
    with open('config.json', 'w') as config:
        json.dump(data, config, indent=4)
    return


def get_targets(category: int, name: str = None):
    targets = []
    data = read_config()
    if category == 0:
        targets = data['0']['pattern']

    elif category == 1 and name is not None:
        if name not in data['1']:
            data['1'][name] = []
        targets = data['1'][name]
    print(targets)

    write_config(data)
    return targets


def custom_click() -> None:
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()


def location_based(targets: list, all_snips) -> None:
    item_dir = read_dict()
    for i in range(3):
        # print(i)
        for j, snip in enumerate(all_snips[i]):
            # print(j)
            for target in targets:
                target_image_path = check_catalogue() + r'\DeadByDaylight\Content\UI\Icons\Items' + item_dir[
                    target] + '.png'
                target_image = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
                r, b, g, a = cv2.split(target_image)
                target_image = cv2.cvtColor(cv2.cvtColor(a, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2GRAY)
                height, width = snip.shape[:2]
                snip = cv2.resize(snip, (1000, height * 1000 // width), interpolation=cv2.INTER_LINEAR)
                # cv2.imshow('Target Image', target_image)
                # cv2.imshow('Snip', snip)
                # cv2.waitKey(500)
                # cv2.destroyAllWindows()
                if TemplateMatch.match_template(snip, target_image):
                    center_point = CropTargets.all_center[i][j]
                    pyautogui.moveTo(center_point[0], center_point[1])
                    print('Target Found!!!')
                    custom_click()
                    pyautogui.moveTo(0, 0)
                    time.sleep(1)
                else:
                    pass
    pyautogui.moveTo(1363, 1146)
    custom_click()
    pyautogui.moveTo(0, 0)


def importance_based(targets: list, all_snips) -> None:
    ...


def check_catalogue() -> str:
    data = read_config()
    if data['game_dir'] == '':
        data['game_dir'] = FindGameDir.get_game_dir()
    write_config(data)
    return data['game_dir']


def click_targets(targets: list, method: int) -> None:
    snips = [[], [], []]
    snips[0], snips[1], snips[2] = CropTargets.get_all()
    if method == 1:
        location_based(targets, snips)
    if method == 2:
        importance_based(targets, snips)


if __name__ == '__main__':
    test1 = get_targets(0)
    get_targets(1, 'The Nurse')

    click_targets(test1, 1)
