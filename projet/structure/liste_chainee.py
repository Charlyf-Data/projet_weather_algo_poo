"""
Linked list implementation module.

Contains:
- Noeud class (node structure)
- ListeChainee class (linked list implementation)
"""

from .base_liste_chainee import BaseListeChainee


class Noeud:  # pylint: disable=too-few-public-methods
    """
    Represents a node in a linked list.
    Stores a value and a reference to the next node.
    """

    def __init__(self, valeur):
        """Initialize node with value and next reference."""
        self.valeur = valeur
        self.prochain = None


class ListeChainee(BaseListeChainee):
    """
    Simple linked list implementation.
    Default behavior is LIFO (stack-like insertion).
    """

    def ajouter(self, valeur):
        """
        Add element at the beginning of the list.
        """
        nouveau_noeud = Noeud(valeur)
        nouveau_noeud.prochain = self.premier
        self.premier = nouveau_noeud

    def retirer(self):
        """
        Remove and return the first element.
        Returns None if list is empty.
        """
        if self.est_vide():
            return None

        valeur = self.premier.valeur
        self.premier = self.premier.prochain
        return valeur

    # -----------------------
    # Additional methods
    # -----------------------

    def ajouter_fin(self, valeur):
        """
        Add element at the end of the list.
        """
        nouveau_noeud = Noeud(valeur)

        if self.premier is None:
            self.premier = nouveau_noeud
            return

        curseur = self.premier
        while curseur.prochain:
            curseur = curseur.prochain

        curseur.prochain = nouveau_noeud

    def retirer_fin(self):
        """
        Remove and return the last element.
        Returns None if list is empty.
        """
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
        """
        Search for a value in the list.
        Returns its position if found, otherwise None.
        """
        curseur = self.premier
        position = 0

        while curseur:
            if curseur.valeur == valeur:
                return position
            curseur = curseur.prochain
            position += 1

        return None
