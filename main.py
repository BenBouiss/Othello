import board_file
import pawn_file
import utils
import Player_file
import GUI
import engine_file
import GUI_pygame
import pygame as p

Game_board = board_file.Board()
Game_board.init_table()
gui_n = GUI.Gui()
gui = GUI_pygame.SCREEN()

ENGINE = engine_file.engine()

#print(Game_board.board.astype(str))
gui_n.Pretty_print(Game_board.board)
print(utils.Convert_str_coord('D4'))


Player_list = []
Player_list.append(Player_file.Joueur_humain('O'))
Player_list.append(Player_file.Joueur_humain('X'))
p.event.wait()
TURN_LIM = 10

def main():
    i=0
    while i<TURN_LIM:

        for event in p.event.get():
            if event.type == p.QUIT:
                i = TURN_LIM
        if i < TURN_LIM:
            Player_list[i%2].Choix_pawn(Game_board)
            #Game_board.print_board()
            gui_n.Pretty_print(Game_board.board)
            gui.update_screen_board(Game_board.board)
            print(f'Score du joueur {i%2 +1} =  {Player_list[i%2].Score}')
            ENGINE.Check_for_end_game(Game_board.board, Player_list[i%2].couleur)
        i+=1
    print(Game_board.board[3][3])
    return 0

def main_pygame():
    i=0
    running = True
    while running:
        Current_player = Player_list[i%2]
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.quit()
            if event.type == p.MOUSEBUTTONUP:
                pos = p.mouse.get_pos()
                x_ind, y_ind = utils.Convert_mouse_pos_x_y_to_ind(pos, GUI_pygame.CELL_WIDTH, GUI_pygame.CELL_HEIGHT)
                print(f'Position moues : {pos}, pos dans index : {(x_ind, y_ind)}')
                flag = Current_player.Choix_pawn_coords(Game_board, (x_ind, y_ind))
                if flag:
                    gui_n.Pretty_print(Game_board.board)
                    gui.update_screen_board(Game_board.board)
                    i+=1
                    print(f'Score du joueur 1 =  {Player_list[0].Score}')
                    print(f'Score du joueur 2 =  {Player_list[1].Score}')
                    for player in Player_list:
                        Permuts = ENGINE.Get_all_permutationAble_squares(Game_board, player.couleur)
                        if len(Permuts) == 0:
                            running = False
                            print(f'No more valid move for player : {player.couleur} ')
                            break
                else:
                    print("Incorrect input please click in a valid location")
                    
    return Player_list
if __name__ == '__main__':
    pass
    p_list = main_pygame()
    print(f'Score history of player 1 {p_list[0].Score_l}')
    print(f'Score history of player 2 {p_list[1].Score_l}')