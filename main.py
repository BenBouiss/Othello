import board_file
import pawn_file
import utils
import Player_file
import GUI

Game_board = board_file.Board()
Game_board.init_table()
gui = GUI.Gui()
#print(Game_board.board.astype(str))
gui.Pretty_print(Game_board.board)
print(utils.Convert_str_coord('D4'))


Player_list = []
Player_list.append(Player_file.Joueur_humain('O'))
Player_list.append(Player_file.Joueur_humain('X'))

for i in range(10):
    Player_list[i%2].Choix_pawn(Game_board)
    #Game_board.print_board()
    gui.Pretty_print(Game_board.board)
print(Game_board.board[3][3])