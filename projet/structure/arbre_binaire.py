"""
Binary tree module.

Provides a simple binary tree implementation
that follows the Collection interface.
"""

from .collection import Collection


class ArbreBinaire(Collection):
    """
    Simple binary tree implementation.

    Each node is itself an ArbreBinaire instance:
    - valeur
    - gauche (left child)
    - droite (right child)
    """

    def __init__(self, valeur=None):
        """Initialize the binary tree node."""
        self.valeur = valeur
        self.gauche = None
        self.droite = None

    # -----------------------
    # Collection methods
    # -----------------------

    def ajouter(self, valeur):
        """
        Add a value to the tree.

        Simple strategy:
        - Fill root
        - Then left
        - Then right
        - Then recurse on left subtree

        This is NOT a binary search tree.
        """
        if self.valeur is None:
            self.valeur = valeur
            return

        if self.gauche is None:
            self.gauche = ArbreBinaire(valeur)
        elif self.droite is None:
            self.droite = ArbreBinaire(valeur)
        else:
            self.gauche.ajouter(valeur)

    def retirer(self):
        """
        Remove the root node.

        Returns the root value or None if empty.
        For simplicity, clears the entire tree.
        """
        if self.est_vide():
            return None

        valeur = self.valeur
        self.valeur = None
        self.gauche = None
        self.droite = None
        return valeur

    def est_vide(self):
        """Return True if the tree is empty."""
        return self.valeur is None

    def as_list(self):
        """
        Return tree values as a list
        using prefix traversal.
        """
        return list(self)

    def __iter__(self):
        """
        Prefix traversal:
        root -> left -> right
        """
        if self.valeur is not None:
            yield self.valeur
        if self.gauche is not None:
            yield from self.gauche
        if self.droite is not None:
            yield from self.droite

    # -----------------------
    # Utility methods
    # -----------------------

    def inserer_gauche(self, valeur):
        """
        Insert a value as direct left child.
        If left child exists, it becomes
        left child of the new node.
        """
        if self.gauche is None:
            self.gauche = ArbreBinaire(valeur)
        else:
            nouveau = ArbreBinaire(valeur)
            nouveau.gauche = self.gauche
            self.gauche = nouveau

    def inserer_droite(self, valeur):
        """
        Insert a value as direct right child.
        If right child exists, it becomes
        right child of the new node.
        """
        if self.droite is None:
            self.droite = ArbreBinaire(valeur)
        else:
            nouveau = ArbreBinaire(valeur)
            nouveau.droite = self.droite
            self.droite = nouveau

    def get_gauche(self):
        """Return left child."""
        return self.gauche

    def get_droite(self):
        """Return right child."""
        return self.droite

    def get_valeur(self):
        """Return node value."""
        return self.valeur
