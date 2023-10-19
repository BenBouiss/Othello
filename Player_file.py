class Joueur(object):
    def __init__(self, couleur):
        self.couleur = couleur



class Joueur_humain(Joueur):
    def __init__(self, couleur):
        super().__init__(couleur)
    
    def Choix_pawn(self, Board):
        Choix = input("Please input coordinates where to put your next pawn (exemple : A1)")
        