import engine_file
import copy
import utils
import pawn_file
import numpy as np
import board_file
import time
import os
import random
from sys import getsizeof

ENGINE = engine_file.engine()

y_center = board_file.LENGTH/2
x_center = board_file.WIDTH/2

Transposition_table_access_counter = 0

Transposition_table = {}


'''
Transposition_table: dict

Key : hash ("Fen" code ex : "3b1q1q/1N2PRQ1/rR3KBr/B4PP1/2Pk1r1b/1P2P1N1/2P2P2/8 X") avec état du board et qui doit bouger
Items : tuple avec en premier le meilleur dplc calculé, en second le score obtenue (>0 : O, <0 : X) et 3ème la depth calculé

'''

HEATMAP = np.zeros((8, 8 ))
for y, row in enumerate(HEATMAP):
    for x, e in enumerate(row):
        HEATMAP[y, x] = min((y-y_center+1)**2, (y-y_center)**2) + min((x-x_center+1)**2, (x-x_center)**2)
        



class Exploration(object):
    def __init__(self):
        pass
        
    def Score_compare(self, Board:object, Joueur_liste: list):
        Score_1 = ENGINE.Count_score(Board, Joueur_liste[0].couleur)
        Score_2 = ENGINE.Count_score(Board, Joueur_liste[1].couleur)
        return Score_1 - Score_2

    def Score(self, Joueur:object):
        #print(Joueur.Score)
        return Joueur.Score

    def Spatial_score_slow(self, Joueur:object, Board: object):
        Score = 0
        for pawn in Board.Pawn_list:
            if pawn.couleur == Joueur.couleur:
                modifier = 1
            else:
                modifier = -1
            x, y = pawn.pos
            Score += HEATMAP[y, x] * modifier

        return Score
    
    def Spatial_score(self, Joueur:object, Board: object):
        Board_mask = Board.Get_board_mask()
        if Joueur.couleur == "X":
            return np.dot(Board_mask.flatten(), HEATMAP.flatten()) *(-1)
        else:
            return np.dot(Board_mask.flatten(), HEATMAP.flatten())
    

    def Explore_moves(self, Board: object, Player: object, Turn : int, Depth, Score_type):
        global DEPTH_MAX, Counter_min_max, Counter_alpha_beta
        DEPTH_MAX = Depth
        Counter_min_max = 0
        #Best_score, Best_move = self.Explore_moves_min_max(Board, Player, Turn, Depth, Score_type)
        

        alpha = -99999
        beta = 99999
        
        Counter_alpha_beta = 0
        Start_alpha_beta = time.time()
        Best_score, Best_move = self.Explore_moves_alpha_beta(Board, Player, Turn, Depth, Score_type, alpha, beta)
        Time_alpha_beta = round(time.time() - Start_alpha_beta, 2)
        os.system('clear')
        #print(f'Best score minmax = {Best_score} Move : {Best_move} n° of branches : {Counter_min_max}')
        print(f'Best score alpha-beta = {Best_score} Move : {Best_move} n° of branches : {Counter_alpha_beta} with depth : {DEPTH_MAX} in : {Time_alpha_beta} s')
        size = getsizeof(Transposition_table)
        print(f'Cached positions : {len(Transposition_table)} / Bite size : {utils.sizeof_fmt(size)}\nNumber of cached positions accessed : {Transposition_table_access_counter}')
        
        return Best_score, Best_move

    def Explore_moves_min_max(self, Board: object, Player: object, Turn : int, Depth, Score_type):
        global Counter_min_max  
        Counter_min_max+=1
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, Player.couleur)
        if Depth == 0 or All_moves == []:
            if Score_type == "Standard":
                return -self.Score(Player)
            if Score_type == "Spatial":
                return -self.Spatial_score(Player, Board)
            
        Scores_l = []
        Max_score = -9999
        random.shuffle(All_moves)
        scores = []
        for moves in All_moves:
            pos_str = utils.Convert_coord_to_string(moves)
            Board.place_pawn(pos_str, Player.couleur)

            Pawn_placed = pawn_file.pawn(Player.couleur, moves)
            permuts = ENGINE.verify_move(Board, Pawn_placed)
            Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)

            Player.Score = ENGINE.Count_score(Board, Player.couleur)
            Player.Score_l.append(self.Score)

            Scores_predi = -self.Explore_moves_min_max(Board, Player, Turn+1, Depth-1, Score_type)
            scores.append(Scores_predi)
            if Scores_predi > Max_score:
                Max_score = Scores_predi
                if Depth == DEPTH_MAX:
                    Next_move = moves

            ### Clean up
            Player.Undo_move()
            Board.remove_pawn(pos_str)
            Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)
        #print(DEPTH_MAX, "xxxxxxxxxxxxxxxxxxxxxxx \n")
        if Depth == DEPTH_MAX:
            #print(f'Turn : {Turn} Decision for player : {Player.couleur} best move : {Next_move} with score {Max_score}, {scores}')
            #input()
            return Max_score, Next_move
        else:
            #print(f'Turn : {Turn} Decision for player : {Player.couleur} with score {Max_score}, {scores}')
            return Max_score
            

        #if len(Scores_l) != 0:
        #    arr = np.array(Scores_l)
        #    if Turn%2 == 0:
        #        Best_score = arr.max()
        #    else:
        #        Best_score = arr.min()

            #Select_mask = arr == Best_score
            #Best_arr = np.array(All_moves)[Select_mask]
            #print(Scores_l, All_moves, Select_mask)
            #rand_ind = np.random.choice(len(Best_arr))
            #Rand_best = Best_arr[rand_ind]
            #print(f'Turn : {Turn} Decision for player : {Player.couleur} best move : {Rand_best} with score {Best_score} \n All other : {All_moves} with scores : {Scores_l}')
            
        

    def Explore_moves_alpha_beta(self, Board: object, Player: object, Turn : int, Depth, Score_type, alpha, beta):
        global Counter_alpha_beta, Transposition_table_access_counter
        Counter_alpha_beta+=1
        
        if Player.Use_transposition:
            fen = Board.Get_fen()
            if fen in Transposition_table:
                if Transposition_table[fen][2] >= Depth:
                    Transposition_table_access_counter+=1
                    return Transposition_table[fen][1], Transposition_table[fen][0]
                
        
        
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, Player.couleur)
        if Depth == 0 or All_moves == []:
            if Score_type == "Standard":
                return -self.Score(Player), None
            if Score_type == "Spatial":
                return -self.Spatial_score(Player, Board), None
            
        Scores_l = []
        Max_score = -9999
        random.shuffle(All_moves)
        for moves in All_moves:
            pos_str = utils.Convert_coord_to_string(moves)
            Board.place_pawn(pos_str, Player.couleur)

            Pawn_placed = pawn_file.pawn(Player.couleur, moves)
            permuts = ENGINE.verify_move(Board, Pawn_placed)
            Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)

            Player.Score = ENGINE.Count_score(Board, Player.couleur)
            Player.Score_l.append(self.Score)
            #print((Board, Player, Turn+1, Depth-1, Score_type, -beta, -alpha))
            Scores_predi, _ = self.Explore_moves_alpha_beta(Board, Player, Turn+1, Depth-1, Score_type, -beta, -alpha)
            Scores_predi*=-1
            ### Clean up
            Player.Undo_move()
            Board.remove_pawn(pos_str)
            Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)
            if Scores_predi > Max_score:
                Max_score = Scores_predi
                Next_move = moves

            if Max_score > alpha:
                alpha = Max_score
            if alpha >= beta:
                break
        
        if Player.Use_transposition:
            fen = Board.Get_fen()
            if not fen in Transposition_table:
                Transposition_table[fen] =  Next_move, Max_score, Depth
            elif Transposition_table[fen][2] < Depth:
                Transposition_table[fen] =  Next_move, Max_score, Depth
        
        if Depth == DEPTH_MAX:
            return Max_score, Next_move
        else:
            return Max_score, None