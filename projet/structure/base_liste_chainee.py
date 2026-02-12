from .collection import Collection


class BaseListeChainee(Collection):
    """
    Classe de base pour toutes les structures basées
    sur une liste chaînée (FIFO, LIFO, etc.).
    Contient la logique commune.
    """

    def __init__(self):
        self.premier = None

    def est_vide(self):
        return self.premier is None

    def as_list(self):
        resultat = []
        curseur = self.premier
        while curseur:
            resultat.append(curseur.valeur)
            curseur = curseur.prochain
        return resultat

    def __iter__(self):
        curseur = self.premier
        while curseur:
            yield curseur.valeur
            curseur = curseur.prochain

    def afficher(self):
        curseur = self.premier
        while curseur:
            print(curseur.valeur, end=" ")
            curseur = curseur.prochain
        print()
