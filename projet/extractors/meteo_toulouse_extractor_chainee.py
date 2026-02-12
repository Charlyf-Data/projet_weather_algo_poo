"""
Meteo Toulouse extractor module.

Specialized extractor for Toulouse OpenData weather API.
"""

# --- Standard library imports ---
from urllib.parse import quote

# --- Third-party imports ---
import pandas as pd

# --- Local imports ---
from .api_extractor import ApiExtractor
from .stations_config import CONFIG_SINGLETON
from .stations_liste import ListeStations, Station


# Load station configuration once (Singleton pattern)
STATIONS_CONFIG_DATA = CONFIG_SINGLETON.get_stations()


class MeteoToulouseExtractorChainnee(ApiExtractor):
    """
    Specialized extractor for Toulouse weather API.
    Inherits from ApiExtractor.
    """

    BASE_URL = (
        "https://data.toulouse-metropole.fr/"
        "api/explore/v2.1/catalog/datasets"
    )

    # Initialize linked list of stations
    STATIONS_LISTE = ListeStations()
    STATIONS_LISTE.charger_depuis_config(STATIONS_CONFIG_DATA)

    @classmethod
    def afficher_stations(cls) -> None:
        """Display all available stations."""
        cls.STATIONS_LISTE.afficher_stations()

    @classmethod
    def get_noms_stations(cls) -> list[str]:
        """Return list of station keys."""
        return [station.cle for station in cls.STATIONS_LISTE]

    def __init__(self, station: str) -> None:
        """Initialize extractor for a given station key."""

        station_obj: Station | None = (
            self.STATIONS_LISTE.trouver_par_cle(station)
        )

        if station_obj is None:
            raise ValueError(f"Station inconnue : {station}")

        self.station_name = station_obj.cle

        sid = station_obj.sid
        ville = station_obj.ville.lower()
        nom_station = station_obj.nom_station.lower()

        dataset_name = (
            f"{sid}-station-meteo-{ville}-{nom_station}"
        )

        dataset_name_encoded = quote(dataset_name, safe="")
        url = f"{self.BASE_URL}/{dataset_name_encoded}/records"

        params = {
            "select": (
                "id,heure_de_paris,humidite,pression,"
                "temperature_en_degre_c"
            ),
            "where": (
                "heure_de_paris >= now(days=-4) "
                "and minute(heure_de_paris)=0 "
                "and (temperature_en_degre_c >= -10 "
                "and temperature_en_degre_c <= 45)"
            ),
            "order_by": "heure_de_paris DESC",
            "limit": "100",
        }

        super().__init__(url, params)

    def to_dataframe(self, data) -> pd.DataFrame:
        """
        Convert API JSON response to DataFrame.
        Extracts 'results' key before conversion.
        """
        if "results" not in data:
            print(
                "Warning: 'results' key missing in JSON response. "
                f"Raw data: {data}"
            )
            return pd.DataFrame()

        return super().to_dataframe(data["results"])
