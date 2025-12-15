# csv_extractor.py
import pandas as pd
from extractors.base_extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    def __init__(self, chemin_fichier: str):
        self.chemin_fichier = chemin_fichier

    def extract(self) -> pd.DataFrame:
        """Lit un CSV et renvoie un DataFrame"""
        try:
            df = pd.read_csv(self.chemin_fichier)
            print("✅ Fichier CSV chargé avec succès")
            return df
        except FileNotFoundError:
            print(f"❌ Fichier introuvable : {self.chemin_fichier}")
            return pd.DataFrame()
