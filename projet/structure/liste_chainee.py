from .base_liste_chainee import BaseListeChainee


class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.prochain = None


class ListeChainee(BaseListeChainee):
    """
    Implémentation d'une liste chaînée simple (LIFO par défaut).
    """

    def ajouter(self, valeur):
        nouveau_noeud = Noeud(valeur)
        nouveau_noeud.prochain = self.premier
        self.premier = nouveau_noeud

    def retirer(self):
        if self.est_vide():
            return None

        valeur = self.premier.valeur
        self.premier = self.premier.prochain
        return valeur

    # -----------------------
    # Méthodes spécifiques
    # -----------------------

    def ajouter_fin(self, valeur):
        nouveau_noeud = Noeud(valeur)

        if self.premier is None:
            self.premier = nouveau_noeud
            return

        curseur = self.premier
        while curseur.prochain:
            curseur = curseur.prochain

        curseur.prochain = nouveau_noeud

    def retirer_fin(self):
        if self.est_vide():
            return None

        if self.premier.prochain is None:
            valeur = self.premier.valeur
            self.premier = None
            return valeur

        curseur = self.premier
        while curseur.prochain.prochain:
            curseur = curseur.prochain

        valeur = curseur.prochain.valeur
        curseur.prochain = None
        return valeur

    def rechercher(self, valeur):
        curseur = self.premier
        position = 0

        while curseur:
            if curseur.valeur == valeur:
                return position
            curseur = curseur.prochain
            position += 1

        return None
