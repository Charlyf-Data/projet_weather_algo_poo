from .collection import Collection


class NoeudFIFO:
    """Noeud simple pour la file FIFO."""
    def __init__(self, valeur):
        self.valeur = valeur
        self.prochain = None


class FileFIFO(Collection):
    """Implémentation minimale d'une file FIFO (First In, First Out)."""

    def __init__(self):
        self.premier = None     # tête
        self.dernier = None     # queue

    def ajouter(self, valeur):
        """Ajoute un élément en queue de file (enqueue)."""
        nouveau = NoeudFIFO(valeur)

        if self.premier is None:
            # File vide
            self.premier = nouveau
            self.dernier = nouveau
        else:
            self.dernier.prochain = nouveau
            self.dernier = nouveau

    def retirer(self):
        """Retire et renvoie l’élément en tête de file (dequeue)."""
        if self.est_vide():
            return None

        valeur = self.premier.valeur
        self.premier = self.premier.prochain

        if self.premier is None:
            self.dernier = None

        return valeur

    def est_vide(self):
        """Retourne True si la file est vide."""
        return self.premier is None

    def as_list(self):
        """Implémentation minimale pour respecter Collection."""
        resultat = []
        curseur = self.premier
        while curseur:
            resultat.append(curseur.valeur)
            curseur = curseur.prochain
        return resultat

    def afficher(self):
        """Affiche le contenu de la file FIFO."""
        curseur = self.premier
        print("FileFIFO:", end=" ")
        while curseur:
            print(curseur.valeur, end=" -> ")
            curseur = curseur.prochain
        print("None")
