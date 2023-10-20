import engine_file as engine
import board_file
import pawn_file
import utils
import GUI
import numpy as np
gui_n = GUI.Gui()
ENGINE = engine.engine()

#BOARD = board_file.Board()



class Joueur(object):
    def __init__(self, couleur):
        self.couleur = couleur
        self.Score = 0
        self.Score_l = []

class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
        self.Type = "Humain"

    def Choix_pawn(self, Board:object):
        self.Choix = input("Please input coordinates where to put your next pawn (exemple : A1):  ")
        Coord = utils.Convert_str_coord(self.Choix)
        Pawn_placed = pawn_file.pawn(self.couleur, Coord)
        self.permuts = ENGINE.verify_move(Board, Pawn_placed)
        #print(permuts, Coord)
        while self.permuts == None or Board.board[Coord[1], Coord[0]] != board_file.NULL_VALUE:
            self.Choix = input("Please input a correct coordinate:  ")
            Coord = utils.Convert_str_coord(self.Choix)
            Pawn_placed = pawn_file.pawn(self.couleur, Coord)
            self.permuts = ENGINE.verify_move(Board, Pawn_placed)

        self.Logic_after_placement(Board)
        #Board.place_pawn(self.Choix, self.couleur)
        #Board, nbr_permutted = ENGINE.Inverts_pawns(Board, self.permuts)
        #self.Score = ENGINE.Count_score(Board, self.couleur)
        #self.Score_l.append(self.Score)
    
    def Logic_after_placement(self, Board):
        Board.place_pawn(self.Choix, self.couleur)
        Board, nbr_permutted = ENGINE.Inverts_pawns(Board, self.permuts)
        self.Score = ENGINE.Count_score(Board, self.couleur)
        self.Score_l.append(self.Score)

    def Make_move(self, Board:object, pos:tuple):
        self.Choix = utils.Convert_coord_to_string(pos)

        Pawn_placed = pawn_file.pawn(self.couleur, pos)
        self.permuts = ENGINE.verify_move(Board, Pawn_placed)
        print(pos)
        if self.permuts == None or Board.board[pos[1], pos[0]] != board_file.NULL_VALUE:
            return False
        else:
            #print('Avant')
            #gui_n.Pretty_print(Board.board)
            #print(self.Choix)
            self.Logic_after_placement(Board)
            #print('Aprés')
            #gui_n.Pretty_print(Board.board)
            #print(f'Permuted coords : {self.permuts}')
            return True
    
class Joueur_ordinateur(Joueur):
    def __init__(self, couleur, Strategy = "Dumb"):
        super().__init__(couleur)
        self.Strategy = Strategy
        self.Type = "AI"

    def Make_move(self, Board:object):
        if self.Strategy== 'Dumb':
            self.Make_move_dumb(Board)

    def Make_move_dumb(self, Board : object):
        
        All_moves = ENGINE.Get_all_permutationAble_squares(Board, self.couleur)

        rand_ind = np.random.choice(len(All_moves))
        Random_move = All_moves[rand_ind]
        #print(f'Selected Move : {Random_move} destination : {Board.board[Random_move[1], Random_move[0]]}')
        pos_str = utils.Convert_coord_to_string(Random_move)
        Board.place_pawn(pos_str, self.couleur)
        Pawn_placed = pawn_file.pawn(self.couleur, Random_move)
        permuts = ENGINE.verify_move(Board, Pawn_placed)

        Board, nbr_permutted = ENGINE.Inverts_pawns(Board, permuts)
        self.Score = ENGINE.Count_score(Board, self.couleur)
        self.Score_l.append(self.Score)
        return True