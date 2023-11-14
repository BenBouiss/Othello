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

    def Explore_moves(self, Board: object, Player: object, Turn : int, Depth, Score_type):
        global DEPTH_MAX, Counter_min_max, Counter_alpha_beta
        DEPTH_MAX = Depth
        Counter_min_max = 0
        #Best_score, Best_move = self.Explore_moves_min_max(Board, Player, Turn, Depth, Score_type)
        #print(f'Best score minmax = {Best_score} Move : {Best_move} n° of branches : {Counter_min_max}')

        alpha = -99999
        beta = 99999
        
        Counter_alpha_beta = 0
        Best_score, Best_move = self.Explore_moves_alpha_beta(Board, Player, Turn, Depth, Score_type, alpha, beta)

        #print(f'Best score alpha-beta = {Best_score} Move : {Best_move} n° of branches : {Counter_alpha_beta}')
        return Best_score, Best_move

    def Explore_moves_min_max(self, Board: object, Player: object, Turn : int, Depth, Score_type):
        global Counter_min_max  
        Counter_min_max+=1
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, Player.couleur)
        if Depth == 0 or All_moves == []:
            if Score_type == "Standard":
                return self.Score(Player)
            if Score_type == "Spatial":
                return self.Spatial_score(Player, Board)
            
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
        global Counter_alpha_beta
        Counter_alpha_beta+=1
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, Player.couleur)
        if Depth == 0 or All_moves == []:
            if Score_type == "Standard":
                return -self.Score(Player)
            if Score_type == "Spatial":
                return -self.Spatial_score(Player, Board)
            
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

            Scores_predi = -self.Explore_moves_alpha_beta(Board, Player, Turn+1, Depth-1, Score_type, -beta, -alpha)

            ### Clean up
            Player.Undo_move()
            Board.remove_pawn(pos_str)
            Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)
            if Scores_predi > Max_score:
                Max_score = Scores_predi
                if Depth == DEPTH_MAX:
                    Next_move = moves

            if Max_score > alpha:
                alpha = Max_score
            if alpha >= beta:
                break

        if Depth == DEPTH_MAX:
            return Max_score, Next_move
        else:
            return Max_score