import board_file
import pawn 

class engine(object):
    def __init__(self):
        pass

    def verify_move(self, Board, pawn : object):
        pass
    
    def Check_for_permut(self, Board, Pawn_placed:object):
        x, y = Pawn_placed.pos
        ### Check in all 8 directions
        Slide_directions = [(-1,-1), (0,-1), (1, -1), (1,0),(1,1), (0,1), (-1,1), (-1,0)]
        Verified_coord_to_invert = []
        for i in range(8):
            sliding = True
            Coord_to_invert = []
            while sliding:
                x_tar, y_tar += (x,y) + Slide_directions[i]
                if 0<= x_tar < board_file.WIDTH and 0<= x_tar < board_file.LENGTH:
                    if Board[y_tar, x_tar].isinstance(pawn.pawn):
                        if Board[y_tar, x_tar].couleur == pawn.Retournement_valeur(Pawn_placed.couleur):
                            Coord_to_invert.append((x_tar, y_tar))
                        else:
                            Verified_coord_to_invert.extend(Coord_to_invert)
                    else:
                        sliding = False
                else: 
                    sliding = False


class Joueur(object):
    def __init__(self, couleur):
        self.couleur = couleur



class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
    
    def Choix_pawn(self, Board):
        Choix = input("Please input coordinates where to put your next pawn (exemple : A1)")
        