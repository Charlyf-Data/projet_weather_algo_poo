# extractors/stations_config.py

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
        # Si déjà initialisé, on sort immédiatement
        if self._initialise:
            return

        # Données de configuration (seulement exécutées la première fois)
        self.stations = {
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
        
        # Marquer comme initialisé
        self._initialise = True

    def get_stations(self):
        """Méthode d'accès simple pour récupérer le dictionnaire de stations."""
        return self.stations

# Création de l'instance Singleton accessible partout dans le module
CONFIG_SINGLETON = Config()