# extractors/meteo_toulouse_extractor.py
from extractors.api_extractor import ApiExtractor

import pandas as pd
from urllib.parse import quote
from extractors.api_extractor import ApiExtractor 

class MeteoToulouseExtractor(ApiExtractor):
    """Spécialisation pour l’API Météo de Toulouse"""

    BASE_URL = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets"

    STATIONS = {
        "montaudran": ("12", "Toulouse", "montaudran"),
        "colomiers_zi_enjacca": ("24", "Colomiers", "zi-enjacca"),
        "parc_maourine": ("62", "Toulouse", "parc-maourine"),
        "marengo": ("2", "Toulouse", "marengo"),
        "pech_david": ("13", "Toulouse", "pech-david"),
        "compans_cafarelli": ("42", "Toulouse", "parc-compans-cafarelli"),
        "fondeyre": ("58", "Toulouse", "fondeyre"),
        "paul_sabatier": ("37", "Toulouse", "universite-paul-sabatier"),
        "mondouzil": ("19", "Mondouzil", "mairie"),
        "basso_cambo": ("8", "Toulouse", "basso-cambo"),
        "soupetard": ("11", "Toulouse", "soupetard"),
        "mons_epuration": ("31", "Mons", "station-epuration"),
        "saint_jory_beldou": ("33", "Saint-Jory", "chapelle-beldou"),
        "jardin_des_plantes": ("38", "Toulouse", "parc-jardin-des-plantes"),
        "la_machine_af": ("48", "Toulouse", "la-machine-af"),
        "life_marechal_juin": ("63", "Toulouse", "life-marechal-juin"),
        "metropole": ("1", "Toulouse", "metropole"),
        "mondonville_ecole": ("20", "Mondonville", "ecole"),
        "teso": ("34", "Toulouse", "teso"),
        "zi_thibaud": ("40", "Toulouse", "zi-thibaud"),
        "busca": ("3", "Toulouse", "busca"),
        "pibrac_bouconne": ("23", "Pibrac", "bouconne-centre-equestre"),
        "life_hall1": ("5", "Toulouse", "life-hall-1"),
        "nakache": ("5", "Toulouse", "nakache"),
        "casselardit": ("41", "Toulouse", "avenue-de-casselardit"),
        "st_exupery": ("45", "Toulouse", "st-exupery"),
    }

    def __init__(self, station: str):
        """Initialise l’extracteur météo pour une station donnée"""
        if station not in self.STATIONS:
            raise ValueError(f"Station inconnue : {station}")

        self.station = station
        sid, ville, nom_station = self.STATIONS[station]


        dataset_name = f"{sid}-station-meteo-{ville.lower()}-{nom_station.lower()}"
        dataset_name_encoded = quote(dataset_name, safe="")
        url = f"{self.BASE_URL}/{dataset_name_encoded}/records"

        # Paramètres API (tu peux les adapter)
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
        return super().to_dataframe(data_json["results"])
