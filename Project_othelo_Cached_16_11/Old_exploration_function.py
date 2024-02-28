import engine_file
import copy
import utils
import pawn_file
import numpy as np
import board_file
import time
import os
import random

ENGINE = engine_file.engine()

y_center = board_file.LENGTH/2
x_center = board_file.WIDTH/2
HEATMAP = np.zeros((8, 8 ))

for y, row in enumerate(HEATMAP):
    for x, e in enumerate(row):
        HEATMAP[y, x] = min((y-y_center+1)**2, (y-y_center)**2) + min((x-x_center+1)**2, (x-x_center)**2)
        
        
        
class Useless():
    def Explore_moves_slow(self, Board: object, Player: object, Turn : int, Depth, Score_type):
        #Current_player = Joueur_liste[Turn%2]
        
        
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, Player.couleur)
        if Depth == 0 or All_moves == []:
            if Score_type == "Standard":
                return self.Score(Player), None
            if Score_type == "Spatial":
                return self.Spatial_score(Player, Board), None
            
        Scores_l = []
        for moves in All_moves:
            Player2 = copy.deepcopy(Player)
            Board2 = copy.deepcopy(Board)
            pos_str = utils.Convert_coord_to_string(moves)
            Board2.place_pawn(pos_str, Player.couleur)

            Pawn_placed = pawn_file.pawn(Player.couleur, moves)
            permuts = ENGINE.verify_move(Board, Pawn_placed)
            Board2, nbr_permutted = ENGINE.Inverts_pawns(Board2, permuts)

            Player2.Score = ENGINE.Count_score(Board2, Player2.couleur)
            Player2.Score_l.append(self.Score)

            Scores_predi, _ = self.Explore_moves(Board2, Player2, Turn+1, Depth-1, Score_type)
            Scores_l.append(Scores_predi)

        if len(Scores_l) != 0:
            arr = np.array(Scores_l)
            if Turn%2 == 0:
                Best_score = arr.max()
            else:
                Best_score = arr.min()

            Select_mask = arr == Best_score
            Best_arr = np.array(All_moves)[Select_mask]
            #print(Scores_l, All_moves, Select_mask)
            rand_ind = np.random.choice(len(Best_arr))
            Rand_best = Best_arr[rand_ind]
            #print(f'Turn : {Turn} Decision for player : {Player.couleur} best move : {Rand_best} with score {Best_score} \n All other : {All_moves} with scores : {Scores_l}')
            return Best_score, Rand_best