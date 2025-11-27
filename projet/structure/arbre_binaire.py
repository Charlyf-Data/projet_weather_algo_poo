from .collection import Collection


class ArbreBinaire(Collection):
    """
    Implémentation simple d'un arbre binaire.
    Chaque noeud est lui-même un ArbreBinaire
    (valeur + enfant gauche + enfant droit).
    """

    def __init__(self, valeur=None):
        self.valeur = valeur
        self.gauche = None
        self.droite = None

    # -----------------------
    # Méthodes "Collection"
    # -----------------------

    def ajouter(self, valeur):
        """
        Ajoute une valeur dans l'arbre.
        Version simple : on remplit la racine, puis gauche, puis droite,
        puis on descend récursivement à gauche.
        Ce n'est PAS un arbre binaire de recherche, juste une structure.
        """
        if self.valeur is None:
            self.valeur = valeur
            return

        if self.gauche is None:
            self.gauche = ArbreBinaire(valeur)
        elif self.droite is None:
            self.droite = ArbreBinaire(valeur)
        else:
            # Si les deux enfants sont déjà remplis,
            # on continue l'insertion dans le sous-arbre gauche.
            self.gauche.ajouter(valeur)

    def retirer(self):
        """
        Retire la racine de l'arbre.
        Renvoie la valeur de la racine, ou None si l'arbre est vide.
        Pour simplifier, on "vide" complètement l'arbre.
        """
        if self.est_vide():
            return None

        valeur = self.valeur
        self.valeur = None
        self.gauche = None
        self.droite = None
        return valeur

    def est_vide(self):
        """
        Renvoie True si l'arbre ne contient aucune valeur.
        """
        return self.valeur is None

    def as_list(self):
        """
        Renvoie les valeurs de l'arbre sous forme de liste
        en utilisant le parcours défini dans __iter__ (préfixe).
        """
        return list(self)

    def __iter__(self):
        """
        Parcours préfixe : racine -> gauche -> droite.
        Permet d'itérer sur l'arbre avec 'for x in arbre:'.
        """
        if self.valeur is not None:
            yield self.valeur
        if self.gauche is not None:
            yield from self.gauche
        if self.droite is not None:
            yield from self.droite

    # -----------------------
    # Méthodes utilitaires
    # -----------------------

    def inserer_gauche(self, valeur):
        """
        Insère une valeur en tant qu'enfant gauche direct.
        Si un enfant gauche existe déjà, il devient enfant gauche du nouveau noeud.
        """
        if self.gauche is None:
            self.gauche = ArbreBinaire(valeur)
        else:
            nouveau = ArbreBinaire(valeur)
            nouveau.gauche = self.gauche
            self.gauche = nouveau

    def inserer_droite(self, valeur):
        """
        Insère une valeur en tant qu'enfant droit direct.
        Si un enfant droit existe déjà, il devient enfant droit du nouveau noeud.
        """
        if self.droite is None:
            self.droite = ArbreBinaire(valeur)
        else:
            nouveau = ArbreBinaire(valeur)
            nouveau.droite = self.droite
            self.droite = nouveau

    def get_gauche(self):
        return self.gauche

    def get_droite(self):
        return self.droite

    def get_valeur(self):
        return self.valeur
