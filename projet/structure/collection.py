from abc import ABC, abstractmethod


class Collection(ABC):
    """
    Classe abstraite représentant une collection d'éléments.
    Toutes les collections qui en héritent doivent implémenter
    les méthodes définir ci-dessous.
    """

    @abstractmethod
    def ajouter(self, valeur):
        """
        Ajoute une valeur dans la collection.
        """
        pass

    @abstractmethod
    def retirer(self):
        """
        Retire un élément de la collection.
        Renvoie la valeur retirée, ou None si la collection est vide.
        """
        pass

    @abstractmethod
    def est_vide(self):
        """
        Renvoie True si la collection est vide, False sinon.
        """
        pass

    @abstractmethod
    def as_list(self):
        """
        Renvoie le contenu de la collection sous forme de liste Python.
        """
        pass

    def __str__(self):
        """
        Affichage commun à toutes les collections :
        nom de la classe + liste des éléments.
        """
        return f"{self.__class__.__name__} : {self.as_list()}"
