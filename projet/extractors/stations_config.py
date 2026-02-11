# extractors/stations_config.py
from projet.extractors.dict_stations import dict_station

class Config:
    """
    Implémentation du pattern Singleton.
    Garantit qu'une seule instance de Config existe et que les données
    de stations ne sont chargées qu'une seule fois.
    """
    _instance = None  # Attribut de classe pour stocker l'instance unique

    def __new__(cls, *args, **kwargs):
        """Contrôle la création de l'instance."""
        if cls._instance is None:
            # Création de l'instance unique
            cls._instance = super(Config, cls).__new__(cls)
            # Drapeau pour l'initialisation unique
            cls._instance._initialise = False 
        
        return cls._instance

    def __init__(self):
        """Initialise les attributs une seule fois."""
        if self._initialise:
            return

        # Données de configuration (seulement exécutées la première fois)
        self.stations = dict_station

        self._initialise = True

    def get_stations(self):
        """Méthode d'accès simple pour récupérer le dictionnaire de stations."""
        return self.stations


CONFIG_SINGLETON = Config()