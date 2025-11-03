# extractors/meteo_toulouse_extractor.py
from extractors.api_extractor import ApiExtractor

class MeteoToulouseExtractor(ApiExtractor):
    """API spécifique à la station Compans-Caffarelli"""
    
    def __init__(self):
        url = (
            "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"
            "42-station-meteo-toulouse-parc-compans-cafarelli/records"
        )
        params = {
            "select": "id,heure_de_paris, humidite, pression, temperature_en_degre_c",
            "where": """heure_de_paris >= now(days=-4)
                        and minute(heure_de_paris)=0
                        and (temperature_en_degre_c >= -10 and temperature_en_degre_c <= 45)""",
            "order_by": "heure_de_paris DESC",
            "limit": "100"
        }
        super().__init__(url, params)

    def to_dataframe(self, data_json):
        return super().to_dataframe(data_json["results"])
