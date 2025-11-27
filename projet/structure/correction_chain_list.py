
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant

    def get_valeur(self):
        return self.valeur

    def get_suivant(self):
        return self.suivant

    def set_suivant(self, suivant):
        self.suivant = suivant


class ListeChainee:
    def __init__(self, premier_maillon:Maillon):
        self.premier_maillon = premier_maillon

    # Ajout d'un maillon en fin de liste
    def ajouter_maillon(self, maillon:Maillon):
        self.get_dernier().set_suivant(maillon)

    # Renvoie le dernier élément de la liste (Celui avec get_suivant() = None)
    def get_dernier(self):
        maillon_actuel = self.premier_maillon

        while maillon_actuel.suivant != None:
            maillon_actuel = maillon_actuel.get_suivant()

        return maillon_actuel

    def afficher_liste(self):
        maillon_actuel = self.premier_maillon

        while maillon_actuel.suivant != None:
            print(maillon_actuel.get_valeur())
            maillon_actuel = maillon_actuel.get_suivant()

        print(maillon_actuel.get_valeur())


premier_maillon = Maillon(0)
ma_liste = ListeChainee(premier_maillon)

ma_liste.ajouter_maillon(Maillon(1))
ma_liste.ajouter_maillon(Maillon(2))
ma_liste.ajouter_maillon(Maillon(3))
ma_liste.ajouter_maillon(Maillon(4))

ma_liste.afficher_liste()