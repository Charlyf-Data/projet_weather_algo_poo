# extractors/meteo_toulouse_extractor.py

from .api_extractor import ApiExtractor
from urllib.parse import quote
from .stations_config import STATIONS
from .stations_liste import ListeStations
import pandas as pd
import requests


class MeteoToulouseExtractorChainnee(ApiExtractor):
    """Spécialisation pour l’API Météo de Toulouse"""

    BASE_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets"

    # Liste chaînée des stations, construite une seule fois
    STATIONS_LISTE = ListeStations()
    STATIONS_LISTE.charger_depuis_config(STATIONS)

    @classmethod
    def afficher_stations(cls):
        """
        Utilitaire pour afficher toutes les stations disponibles.
        """
        cls.STATIONS_LISTE.afficher_stations()

    @classmethod
    def get_noms_stations(cls) -> list[str]:
        """
        Renvoie la liste des clés de stations (ex: ["montaudran", "marengo", ...]).
        Utile pour un menu, un select, etc.
        """
        noms = []
        for station in cls.STATIONS_LISTE:
            noms.append(station.cle)
        return noms

    def __init__(self, station: str):
        """
        Initialise l’extracteur météo pour une station donnée.
        'station' est une clé de STATIONS (ex: "montaudran").
        """
        station_obj = self.STATIONS_LISTE.trouver_par_cle(station)
        if station_obj is None:
            raise ValueError(f"Station inconnue : {station}")

        self.station_name = station_obj.cle
        sid = station_obj.sid
        ville = station_obj.ville
        nom_station = station_obj.nom_station

        dataset_name = f"{sid}-station-meteo-{ville.lower()}-{nom_station.lower()}"
        dataset_name_encoded = quote(dataset_name, safe="")
        url = f"{self.BASE_URL}/{dataset_name_encoded}/records"

        params = {
            "select": "id,heure_de_paris,humidite,pression,temperature_en_degre_c",
            "where": """heure_de_paris >= now(days=-4)
                        and minute(heure_de_paris)=0
                        and (temperature_en_degre_c >= -10 and temperature_en_degre_c <= 45)""",
            "order_by": "heure_de_paris DESC",
            "limit": "100"
        }

        super().__init__(url, params)

    def to_dataframe(self, data_json):
        """Convertit les données JSON en DataFrame Pandas."""
        if "results" not in data_json:
            raise ValueError("Clé 'results' absente du JSON de données.")
        return super().to_dataframe(data_json["results"])
