import string



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