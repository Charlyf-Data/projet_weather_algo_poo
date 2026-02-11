# extractors/stations_liste.py
from ..structure.liste_chainee import ListeChainee



class Station:
    """
    Représente une station météo.
    - cle : clé logique (ex: "montaudran")
    - sid : identifiant numérique en string (ex: "12")
    - ville : nom de la ville (ex: "Toulouse")
    - nom_station : nom de la station dans l'URL (ex: "montaudran")
    """
    def __init__(self, cle: str, sid: str, ville: str, nom_station: str):
        self.cle = cle
        self.sid = sid
        self.ville = ville
        self.nom_station = nom_station

    def __repr__(self) -> str:
        return f"Station(cle={self.cle!r}, ville={self.ville!r}, nom_station={self.nom_station!r})"


class ListeStations(ListeChainee):
    """
    Liste chaînée pour manipuler des Stations.
    """

    def charger_depuis_config(self, config_dict: dict):
        """
        Remplit la liste chaînée à partir du dict STATIONS.
        config_dict: {cle: (sid, ville, nom_station), ...}
        """
        for cle, (sid, ville, nom_station) in config_dict.items():
            self.ajouter_fin(Station(cle, sid, ville, nom_station))

    def trouver_par_cle(self, cle: str) -> Station | None:
        """
        Recherche une station par sa clé (ex: "montaudran").
        Renvoie l'objet Station ou None si non trouvé.
        """
        curseur = self.premier
        while curseur:
            station = curseur.valeur
            if station.cle == cle:
                return station
            curseur = curseur.prochain
        return None

    def afficher_stations(self):
        """
        Affiche toutes les stations sous une forme lisible.
        """
        curseur = self.premier
        while curseur:
            station = curseur.valeur
            print(f"{station.cle} -> {station.ville} - {station.nom_station} (sid={station.sid})")
            curseur = curseur.prochain


