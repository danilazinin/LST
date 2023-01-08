import pathlib
import os.path


def new_entry(text):
    dir_path = pathlib.Path.cwd()
    save_path = os.path.join(str(dir_path) + '/data_file.txt')
    with open(save_path, 'a', encoding='utf-8') as data:
        data.write(f'{text} \n ')


def show_data():
    dir_path = pathlib.Path.cwd()
    save_path = os.path.join(str(dir_path) + '/data_file.txt')
    with open(save_path, 'r', encoding='utf-8') as data:
        names = []
        lines = data.readlines()
        for line in lines:
            if line:
                names.append(line)
        if names[0] == '\n':
            names.pop(0)
    return names