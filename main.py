import board_file
import pawn

Game_board = board_file.Board()
Game_board.init_table()
print(Game_board.board)
print(board_file.Convert_str_coord('D4'))