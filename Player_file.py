import engine_file as engine
import board_file
import pawn_file

ENGINE = engine.engine()
#BOARD = board_file.Board()



class Joueur(object):
    def __init__(self, couleur):
        self.couleur = couleur



class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
    
    def Choix_pawn(self, Board:object):
        Choix = input("Please input coordinates where to put your next pawn (exemple : A1)")
        Coord = board_file.LETTER_TO_COORD_DICT(Choix)
        Pawn_placed = pawn_file.pawn(self.couleur, Coord)
        permuts = ENGINE.verify_move(Board, Pawn_placed)
        while permuts == None and Board.board[Coord[1], Coord[0]] != '':
            Choix = input("Please input a correct coordinate")
            Coord = board_file.LETTER_TO_COORD_DICT(Choix)
            Pawn_placed = pawn_file.pawn(self.couleur, Coord)
            permuts = ENGINE.verify_move(Board, Pawn_placed)

        Board.place_pawn(Choix, self.couleur)
        ENGINE
        