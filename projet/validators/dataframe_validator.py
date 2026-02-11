# validators/dataframe_validator.py
class DataFrameValidator:
    """Valide la cohérence d'un DataFrame"""
    
    @staticmethod
    def validate(df):
        if df.empty:
            raise ValueError("Le DataFrame est vide")
        if "temperature_en_degre_c" not in df.columns:
            raise KeyError("Colonne manquante : temperature_en_degre_c")
        if df["temperature_en_degre_c"].isnull().all():
            raise ValueError("Toutes les températures sont nulles")
        return True
