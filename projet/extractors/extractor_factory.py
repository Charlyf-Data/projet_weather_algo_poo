"""
Extractor factory module.

Provides a factory class for creating different extractor instances.
"""

# --- Local imports ---
from .csv_extractor import CSVExtractor
from .api_extractor import ApiExtractor
from .meteo_toulouse_extractor_chainee import (
    MeteoToulouseExtractorChainnee,
)


class ExtractorFactory:  # pylint: disable=too-few-public-methods
    """
    Factory class used to create extractor instances
    based on a given type.
    """

    @staticmethod
    def get_extractor(extractor_type: str, **kwargs):
        """
        Return an extractor instance based on extractor_type.

        Args:
            extractor_type (str): One of:
                - "csv"
                - "api"
                - "meteo_toulouse"

        Raises:
            ValueError: If required parameters are missing
                        or extractor_type is unknown.
        """

        if extractor_type == "csv":
            chemin_fichier = kwargs.get("chemin_fichier")
            if not chemin_fichier:
                raise ValueError(
                    "Missing 'chemin_fichier' for CSV extractor"
                )
            return CSVExtractor(chemin_fichier)

        if extractor_type == "api":
            url = kwargs.get("url")
            if not url:
                raise ValueError(
                    "Missing 'url' for API extractor"
                )
            params = kwargs.get("params")
            return ApiExtractor(url, params)

        if extractor_type == "meteo_toulouse":
            station = kwargs.get("station")
            if not station:
                raise ValueError(
                    "Missing 'station' for Meteo Toulouse extractor"
                )
            return MeteoToulouseExtractorChainnee(station)

        raise ValueError(
            f"Unknown extractor type: {extractor_type}"
        )

