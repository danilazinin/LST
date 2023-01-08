import os

os.chdir(os.path.dirname(__file__))

from random import randint
import emoji

field = [i for i in range(1, 10)]

emg_x = emoji.emojize(':x:', language='alias')
emg_o = emoji.emojize(':o:', language='alias')


def print_field(f):
    for i in range(len(f)):
        if i % 3 == 0:
            print()
        print(f[i], end='' + '  |  ')
    print()


def your_turn(f, e_x):
    print('Ваш ход')
    print('Выберите  ячейку: ')
    cell = int(input())
    print('Ставим крестик :)')
    index = f.index(cell)
    f[index] = e_x
    print_field(f)
    return f


def computer_turn(f, e_x, e_o):
    print('Мой ход!')
    print('Выбираю ячейку...')
    while True:
        cell = randint(0, 8)
        if f[cell] == e_x or f[cell] == e_o:
            cell = randint(0, 8)
        else:
            f[cell] = e_o
            break
    print_field(f)
    return f


def check_field(f, e_x, e_o):
    win_lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 4, 8),
                 (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8)]
    for line in win_lines:
        if (f[line[0]] == e_x and f[line[1]] == e_x and f[line[2]] == e_x) or (
                f[line[0]] == e_o and f[line[1]] == e_o and f[line[2]] == e_o):
            return False
    else:
        return True


set_digts = set('123456789')
while True:
    computer_turn(field, emg_x, emg_o)
    if not check_field(field, emg_x, emg_o):
        print(emoji.emojize(':hushed:', language='alias'))
        break
    str_field = set(''.join(str(field)))
    if len(set_digts.intersection(str_field)) == 0:
        print('Все ячейки закончились :( \n Ничья!')
        break
    your_turn(field, emg_x)
    if not check_field(field, emg_x, emg_o):
        print(emoji.emojize(':star-struck:', language='alias'))
        break
    str_field = set(''.join(str(field)))
    if len(set_digts.intersection(str_field)) == 0:
        print('Все ячейки закончились :( \n Ничья!')
        break