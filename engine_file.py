import board_file
import pawn_file 
import numpy as np
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
                if 0<= x_tar < board_file.WIDTH and 0<= y_tar < board_file.LENGTH:
                    #print(x_tar, y_tar)
                    #if Board.board[y_tar, x_tar].isinstance(pawn_file.pawn):
                    if Board.board[y_tar, x_tar] != board_file.NULL_VALUE:
                        #print(type(Board.board[y_tar, x_tar]))
                        if Board.board[y_tar, x_tar].couleur == pawn_file.Retournement_valeur(Pawn_placed.couleur):
                            Coord_to_invert.append((x_tar, y_tar))
                        else:
                            Verified_coord_to_invert.extend(Coord_to_invert)
                            sliding = False
                    else:
                        sliding = False
                else: 
                    sliding = False
        return set(Verified_coord_to_invert)
    
    def Inverts_pawns(self, Board: object, List_coord_to_invert:list):
        for coord in List_coord_to_invert:
            x, y = coord
            pawn = Board.board[y, x]
            pawn.retournement()
        return Board, len(List_coord_to_invert)
    
    def Count_score(self, Board:object, couleur:str):
        Counter = 0
        for row in Board.board:
            for e in row:
                if e!= board_file.NULL_VALUE:
                    if e.couleur == couleur:
                        Counter+=1
        return Counter
    
    def Get_all_permutationAble_squares(self, Board:object, couleur:str):
        Coords = np.where(Board.board == board_file.NULL_VALUE)
        valid_placement = []
        x_t, y_t = Coords[1], Coords[0]
        for y, x in zip(x_t, y_t):
            Pawn_placed = pawn_file.pawn(couleur, (x,y))
            Permuts = self.verify_move(Board, Pawn_placed)
            if Permuts != None:
                valid_placement.append((x,y))
        return valid_placement
