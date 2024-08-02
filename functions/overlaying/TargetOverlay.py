import json

import cv2
from PIL import Image


def read_dict():
    with open(r'..\dict.json', 'r') as dic:
        return json.load(dic)


def read_config():
    with open(r'..\config.json', 'r') as conf:
        return json.load(conf)


def get_category_and_dir(dic, target: str):
    for category, inner_dic in dic.items():
        print("Category: ", category, "\nInner_dic: ", inner_dic)
        if target in inner_dic:
            return category, inner_dic[target]
    return None, None


def overlay(background_image_path, overlay_image_path):
    background_image = Image.open(background_image_path)
    # background_image.show()
    overlay_image = Image.open(overlay_image_path)
    overlaid = Image.new('RGBA', background_image.size)
    overlaid.paste(background_image, (0, 0), background_image)
    overlaid.paste(overlay_image, (0, 0), overlay_image)
    overlaid = overlaid.convert('RGB').resize((114, 114)).crop((10, 10, 104, 104))
    # overlaid.resize((128, 128))
    # cropped_overlaid = overlaid.crop((3, 3, 111, 111))
    # cropped_overlaid.show()·
    # overlaid.show()
    return overlaid


if __name__ == '__main__':
    all_dir = read_dict()
    # print(all_dir)
    config = read_config()
    # target_category, target_directory = get_category_and_dir(all_dir, 'iconFavors_bloodyPartyStreamers')
    # directory = str(config['game_dir'])
    # print(directory)
    # print(target_category, target_directory)
    # target_directory = (directory +
    #                     r'\DeadByDaylight\Content\UI\Icons' +
    #                     target_category + target_directory +
    #                     '.png')
    # overlaid_image = overlay(r'.\background\item\RareItem.png', target_directory)
    # overlaid_image = overlay(r'D:\SteamLibrary\steamapps\common\Dead by Daylight\DeadByDaylight\Content\UI\Icons\Favors\Anniversary\iconFavors_bloodyPartyStreamers.png',
    #                          r'E:\PyCharm\Projects\AutoBloodWeb-v0.0.1\functions\overlaying\background\Favors\RareFavor.png')
