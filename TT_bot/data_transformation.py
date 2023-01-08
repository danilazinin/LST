from fractions import Fraction
import pathlib
import csv
import os.path

def converting_to_csv():
    dir_path = pathlib.Path.cwd()
    save_path = os.path.join(str(dir_path) + '/data_file.txt')
    with open(save_path, 'r', encoding='utf-8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(',') for line in stripped if line)
        dir_path = pathlib.Path.cwd()
        save_path = os.path.join(str(dir_path) + '/data_file.csv')
        with open(save_path, 'w', encoding='utf-8') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
def compl(num):
    num = str(num).split()
    left_n = complex(num[0])
    right_n = complex(num[2])
    oper = num[1]
    return left_n, oper, right_n


def ratio_formatting(data):
    data = str(data).split()
    left_value = data[0]
    oper = data[1]
    right_value = data[2]
    a = left_value
    left_value = Fraction(int(a[0: a.index(
        '/')]), int(a[a.index('/')+1:len(a)]))

    g = right_value
    right_value = Fraction(int(g[0: g.index(
        '/')]), int(g[g.index('/')+1:len(g)]))

    return left_value, oper, right_value