import numpy as np
import string
import pawn

WIDTH = 8
LENGTH = 8

LETTER_TO_COORD_DICT = dict()
for index, letter in enumerate(string.ascii_uppercase):
   LETTER_TO_COORD_DICT[letter] = index


def Convert_str_coord(Coord_str:str):
    return LETTER_TO_COORD_DICT[Coord_str[0]], int(Coord_str[1:])-1

class Board(object):
    def __init__(self):
        self.board = np.array([''] * WIDTH * LENGTH).reshape((LENGTH,WIDTH))
        self.Pawn_list = []
    def place_pawn(self, Coord_tar_str, couleur):
        ### le if pour savoir si place libre fais avant normalement
        x, y = Convert_str_coord(Coord_tar_str)
        Pawn = pawn.pawn(couleur, pos = (x, y))
        self.board[y, x] = Pawn
        self.Pawn_list.append(Pawn)

    def init_table(self):
        self.place_pawn('E4', 'O')
        self.place_pawn('D5', 'O')
        self.place_pawn('D4', 'X')
        self.place_pawn('E5', 'X')

    def print_board(self):
        pass