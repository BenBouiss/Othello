def Retournement_valeur(valeur):
    if valeur == 'O':
        return 'X'
    else:
        return 'O'



class pawn(object):
    def __init__(self, couleur, pos:tuple):
        self.couleur = couleur
        self.pos = pos
    def retournement(self):
        self.couleur = Retournement_valeur(self.couleur)
    def __str__(self):
        return self.couleur
    def __int__(self):
        return 1