import board_file
import pawn_file
import utils

Game_board = board_file.Board()
Game_board.init_table()
print(Game_board.board)
print(utils.Convert_str_coord('D4'))