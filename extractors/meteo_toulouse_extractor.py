# extractors/meteo_toulouse_extractor.py
from extractors.api_extractor import ApiExtractor
import pandas as pd
from urllib.parse import quote
from extractors.api_extractor import ApiExtractor 
from .stations_config import STATIONS


class MeteoToulouseExtractor(ApiExtractor):
    """Spécialisation pour l’API Météo de Toulouse"""

    BASE_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets"
    STATIONS = STATIONS  

    def __init__(self, station: str):
        """Initialise l’extracteur météo pour une station donnée"""
        if station not in self.STATIONS:
            raise ValueError(f"Station inconnue : {station}")

        self.station_name = station
        sid, ville, nom_station = self.STATIONS[station]

        dataset_name = f"{sid}-station-meteo-{ville.lower()}-{nom_station.lower()}"
        dataset_name_encoded = quote(dataset_name, safe="")
        url = f"{self.BASE_URL}/{dataset_name_encoded}/records"

        # Paramètres API (ajustables selon besoin)
        params = {
            "select": "id,heure_de_paris,humidite,pression,temperature_en_degre_c",
            "where": """heure_de_paris >= now(days=-4)
                        and minute(heure_de_paris)=0
                        and (temperature_en_degre_c >= -10 and temperature_en_degre_c <= 45)""",
            "order_by": "heure_de_paris DESC",
            "limit": "100"
        }

        # Appel du constructeur parent (ApiExtractor)
        super().__init__(url, params)

    def to_dataframe(self, data_json):
        """Convertit les données JSON en DataFrame Pandas"""
        if "results" not in data_json:
            raise ValueError("Clé 'results' absente du JSON de données.")
        return super().to_dataframe(data_json["results"])