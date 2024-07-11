import json
import re
import winreg


def find_steam_dir():
    try:
        # 打开注册表键
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        # 读取值
        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return install_path
    except FileNotFoundError:
        return None


def read_libraryfolders(steam_dir):
    library_dir = steam_dir + r'\steamapps\libraryfolders.vdf'
    preprocessed_json = preprocessvdf(library_dir)
    final_json = final_standardization(preprocessed_json)
    return final_json


def find_game_dir(json_text):
    data = json.loads(json_text)
    library_path = ''
    # 通过黎明杀机游戏号381210找到安装目录
    for folder in data['libraryfolders'].values():
        if '381210' in folder['apps']:
            library_path = folder['path']
            break
    if library_path != '':
        game_dir = library_path + r'\steamapps\common\Dead by Daylight'
        return game_dir
    else:
        return None


def preprocessvdf(vdf_dir):
    with open(vdf_dir, 'r') as library:
        lines = library.readlines()
        lines.insert(0, '{\n')
        lines.insert(len(lines), '}')
        for i, line in enumerate(lines):
            quote_indices = [index for index, char in enumerate(line) if char == '"']
            if len(quote_indices) >= 2:
                second_quote_index = quote_indices[1]
                line = line[:second_quote_index + 1] + ':' + line[second_quote_index + 1:]
            if len(quote_indices) >= 4:
                fourth_quote_index = quote_indices[3]
                if i + 1 < len(lines) and '}' not in lines[i + 1]:
                    line = line.rstrip('\n') + ',\n'
            lines[i] = line
    return ''.join(lines)


def final_standardization(nonstandard_json):
    pattern = re.compile(r'(["\]}])(\s*)(["\[{])')
    standardized_json = pattern.sub(r'\1,\2\3', nonstandard_json)
    return standardized_json


def get_game_dir():
    return find_game_dir(read_libraryfolders(find_steam_dir()))


if __name__ == '__main__':
    print(f'Dead by Daylight Found at\n{find_game_dir(read_libraryfolders(find_steam_dir()))}')
