# Fichier: extractors/meteo_toulouse_extractor.py (ASSUREZ-VOUS QUE CE CODE EST ENREGISTRÉ)

from .api_extractor import ApiExtractor
from urllib.parse import quote
from .stations_config import CONFIG_SINGLETON 
from .stations_liste import ListeStations, Station 
import pandas as pd
import requests


# Récupération des données de stations à partir de l'instance Singleton
# Cette ligne est exécutée une seule fois au chargement du module
STATIONS_CONFIG_DATA = CONFIG_SINGLETON.get_stations()


class MeteoToulouseExtractorChainnee(ApiExtractor):
    """Spécialisation pour l’API Météo de Toulouse. Hérite d'ApiExtractor."""

    BASE_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets"

    # 1. Initialisation de la liste chaînée en utilisant les données du Singleton
    STATIONS_LISTE = ListeStations()
    STATIONS_LISTE.charger_depuis_config(STATIONS_CONFIG_DATA)

    @classmethod
    def afficher_stations(cls):
        """Affiche toutes les stations disponibles."""
        cls.STATIONS_LISTE.afficher_stations()

    @classmethod
    def get_noms_stations(cls) -> list[str]:
        """Renvoie la liste des clés de stations."""
        return [station.cle for station in cls.STATIONS_LISTE]

    def __init__(self, station: str):
        """Initialise l’extracteur météo pour une station donnée."""
        
        station_obj: Station | None = self.STATIONS_LISTE.trouver_par_cle(station)
        if station_obj is None:
            raise ValueError(f"Station inconnue : {station}")

        self.station_name = station_obj.cle
        sid = station_obj.sid
        ville = station_obj.ville
        nom_station = station_obj.nom_station

        # Construction de l'URL spécifique
        dataset_name = f"{sid}-station-meteo-{ville.lower()}-{nom_station.lower()}"
        dataset_name_encoded = quote(dataset_name, safe="")
        url = f"{self.BASE_URL}/{dataset_name_encoded}/records"

        params = {
            "select": "id,heure_de_paris,humidite,pression,temperature_en_degre_c",
            "where": """heure_de_paris >= now(days=-4) and minute(heure_de_paris)=0 and (temperature_en_degre_c >= -10 and temperature_en_degre_c <= 45)""",
            "order_by": "heure_de_paris DESC",
            "limit": "100"
        }

        super().__init__(url, params)

    def to_dataframe(self, data_json):
        """Convertit les données JSON en DataFrame Pandas, après avoir extrait la clé 'results'."""
        if "results" not in data_json:
            print("Attention: Clé 'results' absente du JSON. Données brutes :", data_json)
            return pd.DataFrame() 
        
        return super().to_dataframe(data_json["results"])