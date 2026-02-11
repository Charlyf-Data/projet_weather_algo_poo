# extractors/api_extractor.py
import requests
from .base_extractor import BaseExtractor

class ApiExtractor(BaseExtractor):
    """Gestion générique des appels API"""
    
    def __init__(self, url, params=None):
        self.url = url
        self.params = params or {}

    def extract(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise Exception(f"Erreur API {response.status_code}: {response.text}")
        return response.json()
        