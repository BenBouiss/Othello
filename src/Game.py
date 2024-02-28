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
from cst import *


#Game_board = board_file.Board()
#Game_board.init_table()

#if GUI_PYGAME_SHOW:
#    gui_n = GUI.Gui()
#    gui = GUI_pygame.SCREEN()

ENGINE = engine_file.engine()

#print(Game_board.board.astype(str))




TURN_LIM = 10

def Deroulement_tour_bot(Player_list, i, gui, Game_board:board_file.Board):
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
        return 0, i
    return 2, i

def Deroulement_tour_humain(Player_list, i, gui, Game_board:board_file.Board):
    Current_player = Player_list[i%2]
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            p.quit()
        if event.type == p.MOUSEBUTTONUP:
            pos = p.mouse.get_pos()
            x_ind, y_ind = utils.Convert_mouse_pos_x_y_to_ind(pos, GUI_pygame.CELL_WIDTH, GUI_pygame.CELL_HEIGHT)
            if x_ind>8 or y_ind>8:
                return 1, i
            print(f'Position moues : {pos}, pos dans index : {(x_ind, y_ind)}')
            flag = Current_player.Make_move(Game_board, (x_ind, y_ind)) ## Makes move and stores the bool in the flag variable True everything good False : error invalid move
            if flag:
                #gui_n.Pretty_print(Game_board.board)
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
# Flag : 0 = GameOver, 1 = Incorrect move, 2 = All good
def main_pygame(Player_list, gui, Game_board:board_file.Board):
    i=0
    running = True
    while running:
        Current_player = Player_list[i%2]
        if Current_player.Type == "Humain":
            Flag, i = Deroulement_tour_humain(Player_list, i, gui, Game_board)
            while Flag == 1:
                Flag, i = Deroulement_tour_humain(Player_list, i, gui, Game_board)
        elif Current_player.Type == "AI":
            #time.sleep(0.5)
            Flag, i = Deroulement_tour_bot(Player_list, i, gui, Game_board)
        if Flag == 0:
            running = False
        #print(Flag, i)
    return Player_list
