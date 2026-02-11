from .csv_extractor import CSVExtractor
from .api_extractor import ApiExtractor
from .meteo_toulouse_extractor_chainee import MeteoToulouseExtractorChainnee

class ExtractorFactory:
    """
    Factory class to create instances of different extractors.
    """
    
    @staticmethod
    def get_extractor(extractor_type: str, **kwargs):
        """
        Factory method to get an extractor instance.
        
        Args:
            extractor_type (str): The type of extractor ('csv', 'api', 'meteo_toulouse').
            **kwargs: Arguments required for the specific extractor.
            
        Returns:
            BaseExtractor: An instance of a class inheriting from BaseExtractor.
            
        Raises:
            ValueError: If the extractor_type is unknown.
        """
        if extractor_type == "csv":
            chemin_fichier = kwargs.get("chemin_fichier")
            if not chemin_fichier:
                raise ValueError("Missing 'chemin_fichier' for CSV extractor")
            return CSVExtractor(chemin_fichier)
            
        elif extractor_type == "api":
            url = kwargs.get("url")
            if not url:
                raise ValueError("Missing 'url' for API extractor")
            params = kwargs.get("params")
            return ApiExtractor(url, params)
            
        elif extractor_type == "meteo_toulouse":
            station = kwargs.get("station")
            if not station:
                raise ValueError("Missing 'station' for Meteo Toulouse extractor")
            return MeteoToulouseExtractorChainnee(station)
            
        else:
            raise ValueError(f"Unknown extractor type: {extractor_type}")
