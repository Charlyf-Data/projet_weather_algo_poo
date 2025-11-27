from .collection import Collection


class Noeud:
    """
    Représente un élément (noeud) de la liste chaînée.
    Chaque noeud contient une valeur et une référence vers le prochain nœud.
    """
    def __init__(self, valeur):
        self.valeur = valeur
        self.prochain = None


class ListeChainee(Collection):
    """
    Implémentation d'une liste chaînée simple.
    Hérite de la classe abstraite Collection.
    """

    def __init__(self):
        # Référence vers le premier nœud de la liste
        self.premier = None

    # -----------------------
    # Méthodes "Collection"
    # -----------------------

    def ajouter(self, valeur):
        """
        Ajoute un élément au début de la liste.
        Implémente la méthode abstraite 'ajouter' de Collection.
        """
        nouveau_noeud = Noeud(valeur)
        nouveau_noeud.prochain = self.premier
        self.premier = nouveau_noeud

    def retirer(self):
        """
        Retire l'élément au début de la liste.
        Renvoie la valeur retirée, ou None si la liste est vide.
        """
        if self.est_vide():
            return None

        valeur = self.premier.valeur
        self.premier = self.premier.prochain
        return valeur

    def est_vide(self):
        """
        Renvoie True si la liste est vide, False sinon.
        """
        return self.premier is None

    def as_list(self):
        """
        Renvoie le contenu de la liste chaînée
        sous forme de liste Python classique.
        """
        resultat = []
        curseur = self.premier
        while curseur:
            resultat.append(curseur.valeur)
            curseur = curseur.prochain
        return resultat

    def __iter__(self):
        """
        Permet d'itérer sur la liste chaînée avec 'for x in liste:'.
        """
        curseur = self.premier
        while curseur:
            yield curseur.valeur
            curseur = curseur.prochain

    # -----------------------
    # Méthodes utilitaires
    # -----------------------

    def ajouter_fin(self, valeur):
        """
        Ajoute un élément à la fin de la liste.
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
        Retire le dernier élément de la liste.
        Renvoie la valeur retirée, ou None si la liste est vide.
        """
        if self.est_vide():
            return None

        # Un seul élément
        if self.premier.prochain is None:
            valeur = self.premier.valeur
            self.premier = None
            return valeur

        # Plusieurs éléments
        curseur = self.premier
        while curseur.prochain.prochain:
            curseur = curseur.prochain

        valeur = curseur.prochain.valeur
        curseur.prochain = None
        return valeur

    def rechercher(self, valeur):
        """
        Recherche une valeur dans la liste.
        Renvoie l'indice (position) si trouvée, sinon None.
        """
        curseur = self.premier
        position = 0

        while curseur:
            if curseur.valeur == valeur:
                return position
            curseur = curseur.prochain
            position += 1

        return None

    def afficher(self):
        """
        Affiche les valeurs de la liste sur une seule ligne.
        """
        curseur = self.premier
        while curseur:
            print(curseur.valeur, end=" ")
            curseur = curseur.prochain
        print()
