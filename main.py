import board_file
import pawn_file
import utils
import Player_file
import GUI
import engine_file
import GUI_pygame
import pygame as p
import time
import pandas as pd
import os
import cProfile


GUI_PYGAME_SHOW = True
PRINT_SHOW = False
SAVE_CSV_FILE = False
RUN_CPROFILER = True

Game_board = board_file.Board()
Game_board.init_table()

#if GUI_PYGAME_SHOW:
#    gui_n = GUI.Gui()
#    gui = GUI_pygame.SCREEN()

ENGINE = engine_file.engine()

#print(Game_board.board.astype(str))
if PRINT_SHOW:
    gui_n.Pretty_print(Game_board.board)
    print(utils.Convert_str_coord('D4'))



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
    print(Game_board.board[3][3])
    return 0


def Deroulement_tour_bot(Player_list, i):
    Current_player = Player_list[i%2]
    Current_player.Make_move(Game_board, Current_player)
    if GUI_PYGAME_SHOW:
        gui.update_screen_board(Game_board.board)
    i+=1
    player_check = Player_list[i%2]
    Permuts = ENGINE.Get_all_permutationAble_squares(Game_board, player_check.couleur)
    if len(Permuts) == 0:
        if PRINT_SHOW:
            print(f'No more valid move for player : {player_check.couleur} ')
        p.quit()
        return 0, i
    return 2, i

def Deroulement_tour_humain(Player_list, i):
    Current_player = Player_list[i%2]
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            p.quit()
        if event.type == p.MOUSEBUTTONUP:
            pos = p.mouse.get_pos()
            x_ind, y_ind = utils.Convert_mouse_pos_x_y_to_ind(pos, GUI_pygame.CELL_WIDTH, GUI_pygame.CELL_HEIGHT)
            print(f'Position moues : {pos}, pos dans index : {(x_ind, y_ind)}')
            flag = Current_player.Make_move(Game_board, (x_ind, y_ind)) ## Makes move and stores the bool in the flag variable True everything good False : error invalid move
            if flag:
                if Current_player.Type == "Humain":
                    gui_n.Pretty_print(Game_board.board)
                gui.update_screen_board(Game_board.board)
                i+=1
                print(f'Score du joueur 1 =  {Player_list[0].Score}')
                print(f'Score du joueur 2 =  {Player_list[1].Score}')
                player_check = Player_list[i%2]
                Permuts = ENGINE.Get_all_permutationAble_squares(Game_board, player_check.couleur)
                if len(Permuts) == 0:
                    running = False
                    print(f'No more valid move for player : {player_check.couleur} ')
                    p.quit()
                    return 0, i
                return 2, i
            else:
                print("Incorrect input please click in a valid location")
                return 1, i
    return 2, i
# 0 = GameOver, 1 = Incorrect move, 2 = All good
def main_pygame():
    i=0
    running = True
    while running:
        Current_player = Player_list[i%2]
        
        if Current_player.Type == "Humain":
            Flag, i = Deroulement_tour_humain(Player_list, i)
            while Flag == 1:
                Flag, i = Deroulement_tour_humain(Player_list, i)
        elif Current_player.Type == "AI":
            #time.sleep(0.5)
            Flag, i = Deroulement_tour_bot(Player_list, i)
            
        if Flag == 0:
            running = False
        #print(Flag, i)
    return Player_list

if __name__ == '__main__':
    i = 0
    col_names = ["Id_joueur", "Strategy","Depth", "Max_Score","History"]
    df = pd.DataFrame(columns = col_names)
    Nbr_iter = 20
    print(f'Starting {Nbr_iter} iterations')
    while i<Nbr_iter:
        print(f'Starting {i} : {Nbr_iter} iterations', end = "\r")
        if GUI_PYGAME_SHOW:
            gui_n = GUI.Gui()
            gui = GUI_pygame.SCREEN()
        ENGINE = engine_file.engine()

        Player_list = []
        
        ### Ordinateur exploration depth 4 contre version spatial exploration
        Player_list.append(Player_file.Joueur_ordinateur('O', Strategy="Exploration", Depth=4))
        Player_list.append(Player_file.Joueur_ordinateur('X', Strategy="Exploration_spatial", Depth=4))

        ### Joueur contre Joueur
        #Player_list.append(Player_file.Joueur_humain('O'))
        #Player_list.append(Player_file.Joueur_humain('X'))

        ### Ordinateur méthode exploration(O) vs humain(X)
        #Player_list.append(Player_file.Joueur_ordinateur('O', Strategy="Exploration", Depth=3))
        #Player_list.append(Player_file.Joueur_humain('X'))

        ### Dumb vs Dumb
        #Player_list.append(Player_file.Joueur_ordinateur('O'))
        #Player_list.append(Player_file.Joueur_ordinateur('X'))

        ### Humain(O) vs dumb(X)
        #Player_list.append(Player_file.Joueur_humain('O'))
        #Player_list.append(Player_file.Joueur_ordinateur('X'))

        Game_board = board_file.Board()
        Game_board.init_table()
        if RUN_CPROFILER:
            prof = cProfile.Profile()
            with cProfile.Profile() as pr:
                p_list = main_pygame()
            df = pd.DataFrame(pr.getstats(),
            columns=['func', 'ncalls', 'ccalls', 'tottime', 'cumtime', 'callers']
            ).sort_values(by = "cumtime", ascending=False)
            df.to_csv()
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

            print(__location__)
            df.to_csv(os.path.join(__location__, f'Stat_store/Function_call_{int(time.time())}_iter_{int(len(df)/2)}.csv'))
            
        else:
            p_list = main_pygame()
        i+=1
        if PRINT_SHOW:
            print(f'Score history of player 1 {p_list[0].Score_l}')
            print(f'Score history of player 2 {p_list[1].Score_l}')

        if SAVE_CSV_FILE:
            df = pd.concat([df, pd.DataFrame(
                [['1', p_list[0].Strategy, p_list[0].Depth , p_list[0].Score, p_list[0].Score_l]],columns = col_names
            )], ignore_index = True)
            
            df = pd.concat([df, pd.DataFrame(
                [['2', p_list[1].Strategy, p_list[1].Depth, p_list[1].Score, p_list[1].Score_l]],columns = col_names
            )], ignore_index = True)
            
    if SAVE_CSV_FILE:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        print(__location__)
        df.to_csv(os.path.join(__location__, f'Stat_store/Stat_{int(time.time())}_iter_{int(len(df)/2)}.csv'))
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        print(__location__)