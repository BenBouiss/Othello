import board_file
import pawn_file 

class engine(object):
    def __init__(self):
        pass

    def verify_move(self, Board:object, Pawn_placed : object):
        Verified_coord_to_invert = self.Check_for_permut(Board, Pawn_placed)
        if len(Verified_coord_to_invert) == 0:
            return None
        else:
            return Verified_coord_to_invert
        
    def Check_for_permut(self, Board:object, Pawn_placed:object):
        x, y = Pawn_placed.pos
        ### Check in all 8 directions
        Slide_directions = [(-1,-1), (0,-1), (1, -1), (1,0),(1,1), (0,1), (-1,1), (-1,0)]
        Verified_coord_to_invert = []
        for i in range(8):
            sliding = True
            Coord_to_invert = []
            x_tar, y_tar = x, y
            while sliding:
                x_tar += Slide_directions[i][0]
                y_tar += Slide_directions[i][1]
                #print(Board.board[y_tar, x_tar])
                if 0<= x_tar < board_file.WIDTH and 0<= x_tar < board_file.LENGTH:
                    #if Board.board[y_tar, x_tar].isinstance(pawn_file.pawn):
                    if Board.board[y_tar, x_tar] != board_file.NULL_VALUE:
                        #print(type(Board.board[y_tar, x_tar]))
                        if Board.board[y_tar, x_tar].couleur == pawn_file.Retournement_valeur(Pawn_placed.couleur):
                            Coord_to_invert.append((x_tar, y_tar))
                        else:
                            Verified_coord_to_invert.extend(Coord_to_invert)
                    else:
                        sliding = False
                else: 
                    sliding = False
        return Verified_coord_to_invert
    
    def Inverts_pawns(self, Board: object, List_coord_to_invert:list):
        for coord in List_coord_to_invert:
            x, y = coord
            pawn = Board.board[y, x]
            pawn.retournement()
        return Board
