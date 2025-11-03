# extractors/base_extractor.py
from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    """Classe de base pour tous les extracteurs de données"""

    @abstractmethod
    def extract(self):
        """Méthode d'extraction à implémenter"""
        pass

    def to_dataframe(self, data):
        """Méthode commune de conversion"""
        return pd.DataFrame(data)
