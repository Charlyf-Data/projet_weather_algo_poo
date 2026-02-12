from .base_liste_chainee import BaseListeChainee


class NoeudFIFO:
    """Noeud simple pour la file FIFO."""
    def __init__(self, valeur):
        self.valeur = valeur
        self.prochain = None


class FileFIFO(BaseListeChainee):
    """
    Implémentation d'une file FIFO (First In, First Out).
    """

    def __init__(self):
        super().__init__()
        self.dernier = None  # pointeur de queue

    # -----------------------
    # Méthodes Collection
    # -----------------------

    def ajouter(self, valeur):
        """
        Ajoute un élément en queue de file (enqueue).
        """
        nouveau = NoeudFIFO(valeur)

        if self.premier is None:
            self.premier = nouveau
            self.dernier = nouveau
        else:
            self.dernier.prochain = nouveau
            self.dernier = nouveau

    def retirer(self):
        """
        Retire et renvoie l’élément en tête de file (dequeue).
        """
        if self.est_vide():
            return None

        valeur = self.premier.valeur
        self.premier = self.premier.prochain

        if self.premier is None:
            self.dernier = None

        return valeur

    # -----------------------
    # Méthode spécifique affichage FIFO
    # -----------------------

    def afficher(self):
        """
        Affichage spécifique FIFO.
        """
        curseur = self.premier
        print("FileFIFO:", end=" ")
        while curseur:
            print(curseur.valeur, end=" -> ")
            curseur = curseur.prochain
        print("None")
