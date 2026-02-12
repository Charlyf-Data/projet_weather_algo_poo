"""
DataFrame validation module.

Provides validation utilities for meteorological DataFrames.
"""


class DataFrameValidator:  # pylint: disable=too-few-public-methods
    """
    Utility class for validating pandas DataFrames.
    """

    @staticmethod
    def validate(df):
        """
        Validate DataFrame consistency.

        Checks:
        - DataFrame is not empty
        - Required column exists
        - Temperature column is not entirely null

        Raises:
            ValueError: If DataFrame is empty or invalid
            KeyError: If required column is missing
        """
        if df.empty:
            raise ValueError("Le DataFrame est vide")

        if "temperature_en_degre_c" not in df.columns:
            raise KeyError(
                "Colonne manquante : temperature_en_degre_c"
            )

        if df["temperature_en_degre_c"].isnull().all():
            raise ValueError(
                "Toutes les températures sont nulles"
            )

        return True
