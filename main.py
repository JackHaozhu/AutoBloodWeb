import functions.FindGameDir
import functions.TemplateMatching
import functions.overlaying.TargetOverlay
from functions import FindGameDir

import json
import cv2
import numpy as np
from PIL import Image


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
                    print('Target Directory: ', target_full_dir)
                    print('Background Path: ', background_path)
                    overlaid_image = functions.overlaying.TargetOverlay.overlay(background_path, target_full_dir)
                    template_images.append(pil2opencv(overlaid_image))



def click_targets(target_positions):
    ...


if __name__ == '__main__':
    config = read_config()
    dir_dict = read_dict()
    if config['game_dir'] == '':
        config['game_dir'] = functions.FindGameDir.get_game_dir()
        write_config(config)
    get_template_images('0')
