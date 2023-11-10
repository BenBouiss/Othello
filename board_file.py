import numpy as np
import string
import pawn_file
import utils

WIDTH = 8
LENGTH = 8

NULL_VALUE = ' '
value_mask = {
            "O" : 1,
            "X" : -1
        }
class Board(object):
    def __init__(self):
        self.board = np.array([NULL_VALUE] * WIDTH * LENGTH).reshape((LENGTH,WIDTH)).astype(dtype='object')
        self.Pawn_list = []
    def place_pawn(self, Coord_tar_str, couleur):
        ### le if pour savoir si place libre fais avant normalement
        x, y = utils.Convert_str_coord(Coord_tar_str)
        Pawn = pawn_file.pawn(couleur, pos = (x, y))
        self.board[y, x] = Pawn
        self.Pawn_list.append(Pawn)

    def remove_pawn(self, Coord_tar_str):
        x, y = utils.Convert_str_coord(Coord_tar_str)
        self.board[y, x] = NULL_VALUE

    def init_table(self):
        self.place_pawn('E4', 'O')
        self.place_pawn('D5', 'O')
        self.place_pawn('D4', 'X')
        self.place_pawn('E5', 'X')

    def print_board(self):
        print(self.board.astype(str))
        
    def Get_board_mask(self):
        b = self.board.astype(str)
        tmp = np.zeros(b.shape)
        for i, e in enumerate(np.unique(b)):
            if e!= NULL_VALUE:
                tmp[b==e] = value_mask[e]
        return tmp
