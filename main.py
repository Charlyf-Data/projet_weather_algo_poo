from extractors.meteo_toulouse_extractor import MeteoToulouseExtractor
from validators.dataframe_validator import DataFrameValidator

def main():
    extractor = MeteoToulouseExtractor()
    data_json = extractor.extract()
    df = extractor.to_dataframe(data_json)

    # Validation
    try:
        DataFrameValidator.validate(df)
        print("✅ Données valides :", len(df), "lignes")
        print(df.head())
    except Exception as e:
        print("❌ Erreur :", e)

if __name__ == "__main__":
    main()
