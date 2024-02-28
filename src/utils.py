import string
import pandas as pd


LETTER_TO_COORD_DICT = dict()
for index, letter in enumerate(string.ascii_uppercase):
   LETTER_TO_COORD_DICT[letter] = index

def Convert_str_coord(Coord_str:str):
    return LETTER_TO_COORD_DICT[Coord_str[0]], int(Coord_str[1:])-1

def Convert_coord_to_string(pos:tuple):
    return f'{string.ascii_uppercase[pos[0]]}{pos[1]+1}'

def Convert_mouse_pos_x_y_to_ind(pos: tuple, CELL_WIDTH = 64, CELL_HEIGHT = 64):
    x, y= pos
    return x // CELL_WIDTH, y // CELL_HEIGHT

def Convert_cprofile_to_dataframe(profiler_results):
    data=[]
    started=False

    for l in profiler_results.stdout.split("\n"):
        if not started:
            if l=="   ncalls  tottime  percall  cumtime  percall filename:lineno(function)":
                started=True
                data.append(l)
        else:
            data.append(l)
    content=[]
    for l in data:
        fs = l.find(" ",8)
        content.append(tuple([l[0:fs] , l[fs:fs+9], l[fs+9:fs+18], l[fs+18:fs+27], l[fs+27:fs+36], l[fs+36:]]))
    prof_df = pd.DataFrame(content[1:], columns=content[0])
    return prof_df

def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)
