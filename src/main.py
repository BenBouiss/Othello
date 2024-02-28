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
import Game
from Game import main_pygame
from cst import *
 
#GUI_PYGAME_SHOW = True
#PRINT_SHOW = False
#SAVE_CSV_FILE = True
#RUN_CPROFILER = False

#if GUI_PYGAME_SHOW:
#    gui_n = GUI.Gui()
#    gui = GUI_pygame.SCREEN()

#print(Game_board.board.astype(str))
#if PRINT_SHOW:
#    gui_n.Pretty_print(Game_board.board)
#    print(utils.Convert_str_coord('D4'))

def p_list_to_df(df_csv, p_list:list):
    df_csv = pd.concat([df_csv, pd.DataFrame(
                [['1', p_list[0].Strategy, p_list[0].Depth , p_list[0].Score, p_list[0].Score_l]],columns = col_names
            )], ignore_index = True)
            
    df_csv = pd.concat([df_csv, pd.DataFrame(
            [['2', p_list[1].Strategy, p_list[1].Depth, p_list[1].Score, p_list[1].Score_l]],columns = col_names
            )], ignore_index = True)
    return df_csv

def save_df_p_list_to_csv(df_csv):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    df_csv.to_csv(os.path.join(__location__, f'../Stat_store/Stat_{int(time.time())}_iter_{int(len(df_csv)/2)}.csv'))
    print(__location__)

if __name__ == '__main__':
    i = 0
    col_names = ["Id_joueur", "Strategy","Depth", "Max_Score","History"]
    df_csv = pd.DataFrame(columns = col_names)
    Nbr_iter = 200
    print(f'Starting {Nbr_iter} iterations')
    if GUI_PYGAME_SHOW:
        gui_n = GUI.Gui()
        gui = GUI_pygame.SCREEN()
        
    while i<Nbr_iter:
        print(f'Starting {i} : {Nbr_iter} iterations')
        ENGINE = engine_file.engine()

        Player_list = []
        
        ### Ordinateur exploration depth 4 contre version spatial exploration
        Player_list.append(Player_file.Joueur_ordinateur('O', Strategy="Exploration", Depth=5, Use_transposition=True))
        Player_list.append(Player_file.Joueur_ordinateur('X'))
        #Player_list.append(Player_file.Joueur_ordinateur('X', Strategy="Exploration_spatial", Depth=3))


        Game_board = board_file.Board()
        Game_board.init_table()
        Game_board.print_board()
        if RUN_CPROFILER:
            prof = cProfile.Profile()
            with cProfile.Profile() as pr:
                p_list = main_pygame(Player_list, gui, Game_board)
            df = pd.DataFrame(pr.getstats(),
            columns=['func', 'ncalls', 'ccalls', 'tottime', 'cumtime', 'callers']
            ).sort_values(by = "cumtime", ascending=False)
            #df.to_csv()
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

            print(__location__)
            df.to_csv(os.path.join(__location__, f'../Stat_store/Function_call_{int(time.time())}_iter_{int(len(df)/2)}.csv'))
            
        else:
            p_list = main_pygame(Player_list, gui, Game_board)
        print("End of game")
        GUI_pygame.init(gui.screen)
        
        i+=1
        if PRINT_SHOW:
            print(f'Score history of player 1 {p_list[0].Score_l}')
            print(f'Score history of player 2 {p_list[1].Score_l}')

        if SAVE_CSV_FILE:
            df_csv = p_list_to_df(df_csv, p_list)
    p.quit()        
    if SAVE_CSV_FILE:
        save_df_p_list_to_csv(df_csv)
