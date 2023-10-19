import engine_file as engine
import board_file
import pawn_file
import utils
ENGINE = engine.engine()
#BOARD = board_file.Board()



class Joueur(object):
    def __init__(self, couleur):
        self.couleur = couleur
        self.Score = 0


class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
    
    def Choix_pawn(self, Board:object):
        Choix = input("Please input coordinates where to put your next pawn (exemple : A1):  ")
        Coord = utils.Convert_str_coord(Choix)
        Pawn_placed = pawn_file.pawn(self.couleur, Coord)
        permuts = ENGINE.verify_move(Board, Pawn_placed)
        #print(permuts, Coord)
        while permuts == None or Board.board[Coord[1], Coord[0]] != board_file.NULL_VALUE:
            Choix = input("Please input a correct coordinate:  ")
            Coord = utils.Convert_str_coord(Choix)
            Pawn_placed = pawn_file.pawn(self.couleur, Coord)
            permuts = ENGINE.verify_move(Board, Pawn_placed)

        Board.place_pawn(Choix, self.couleur)
        Board = ENGINE.Inverts_pawns(Board, permuts)
        