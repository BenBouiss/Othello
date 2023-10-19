import string

LETTER_TO_COORD_DICT = dict()
for index, letter in enumerate(string.ascii_uppercase):
   LETTER_TO_COORD_DICT[letter] = index

def Convert_str_coord(Coord_str:str):
    return LETTER_TO_COORD_DICT[Coord_str[0]], int(Coord_str[1:])-1
