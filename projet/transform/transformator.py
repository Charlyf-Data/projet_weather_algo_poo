"""
Module de transformation des données météo.

Ce module permet :
- L'extraction multi-stations
- La validation des données
- La fusion
- La sauvegarde CSV avec contrôle des doublons
"""

# Standard library
import os
from abc import ABC, abstractmethod

# Third party
import pandas as pd

# Local imports
from ..extractors.meteo_toulouse_extractor_chainee import (
    MeteoToulouseExtractorChainnee,
)
from ..validators.dataframe_validator import DataFrameValidator


# -------------------------------------------------
# Classe mère abstraite
# -------------------------------------------------
class Transform(ABC):
    """Classe abstraite définissant le contrat des transformations."""

    @abstractmethod
    def run(self):
        """Méthode principale à implémenter."""
        raise NotImplementedError


# -------------------------------------------------
# Classe fille : CSV Transform
# -------------------------------------------------
class CsvTransform(Transform):
    """
    Extraction, validation, fusion et sauvegarde
    des données météo de toutes les stations.
    """

    def __init__(self, key_cols: list[str] | None = None):
        """
        key_cols : colonnes servant à détecter
        les doublons lors de la sauvegarde.
        """
        self.key_cols = key_cols or ["heure_de_paris"]
        self.df = pd.DataFrame()

    # -------------------------------------------------
    # Étape 1 — Extraction et fusion
    # -------------------------------------------------
    def extract_all_stations(self) -> pd.DataFrame:
        """Extrait et fusionne toutes les stations disponibles."""
        list_df = []

        # On récupère les noms via la classe chainée
        stations = MeteoToulouseExtractorChainnee.get_noms_stations()

        for station in stations:
            try:
                print(f"Extraction en cours pour : {station}")

                extractor = MeteoToulouseExtractorChainnee(station)
                data_json = extractor.extract()
                df_station = extractor.to_dataframe(data_json)

                DataFrameValidator.validate(df_station)

                df_station["station_name"] = station
                list_df.append(df_station)

            except ValueError as error:
                print(f"Erreur pour {station} ignorée : {error}")

        if list_df:
            self.df = pd.concat(list_df, ignore_index=True)
            print(f"Fusion terminée : {len(self.df)} lignes au total.")
        else:
            print("Aucune donnée extraite.")
            self.df = pd.DataFrame()

        return self.df

    # -------------------------------------------------
    # Étape 2 — Implémentation run
    # -------------------------------------------------
    def run(self) -> pd.DataFrame:
        """Pipeline principal d'extraction."""
        print("Démarrage du pipeline CSV multi-stations.")
        return self.extract_all_stations()

    # -------------------------------------------------
    # Étape 3 — Sauvegarde CSV
    # -------------------------------------------------
    def save_to_csv(
        self,
        dir_path: str = "data_meteo_toulouse_station",
    ) -> str:
        """
        Sauvegarde le DataFrame en CSV.
        Si le fichier existe, seules les nouvelles
        lignes uniques sont ajoutées.
        """
        os.makedirs(dir_path, exist_ok=True)

        filename = "data_all_stations.csv"
        path = os.path.join(dir_path, filename)

        if os.path.exists(path):
            old_df = pd.read_csv(path)
            merged_df = pd.concat([old_df, self.df], ignore_index=True)
            merged_df.drop_duplicates(
                subset=self.key_cols,
                inplace=True,
            )
            merged_df.to_csv(path, index=False)

            diff = len(merged_df) - len(old_df)
            print(
                f"Mise à jour : {diff} nouvelles lignes "
                f"(total {len(merged_df)})."
            )
        else:
            self.df.to_csv(path, index=False)
            print(
                f"Nouveau fichier créé : {path} "
                f"({len(self.df)} lignes)."
            )

        return path

    # -------------------------------------------------
    # Étape 4 — Pipeline complet
    # -------------------------------------------------
    def run_and_save(
        self,
        dir_path: str = "data_meteo_toulouse_station",
    ) -> str:
        """Exécute extraction + sauvegarde."""
        self.run()
        return self.save_to_csv(dir_path)
