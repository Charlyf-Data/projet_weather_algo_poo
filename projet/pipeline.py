from .extractors.extractor_factory import ExtractorFactory
from .validators.dataframe_validator import DataFrameValidator
from .decorators import log_execution_time  # Import du décorateur
import pandas as pd

class Pipeline:
    """
    Represents a data processing pipeline.
    """
    def __init__(self):
        self.extractor = None
        self.validator = None
        self.saver = None

    def set_extractor(self, extractor):
        self.extractor = extractor

    def set_validator(self, validator):
        self.validator = validator

    def set_saver(self, saver):
        self.saver = saver

    @log_execution_time  # Utilisation du décorateur
    def run(self):
        """
        Executes the pipeline: Extract -> Validate -> Save
        """
        print("[Pipeline] Starting Pipeline...")
        
        # 1. Extraction
        if not self.extractor:
            raise ValueError("No extractor set in pipeline!")
            
        print(f"[Pipeline] Extracting data using {self.extractor.__class__.__name__}...")
        raw_data = self.extractor.extract()
        df = self.extractor.to_dataframe(raw_data)
        print(f"[Pipeline] Extraction complete. DataFrame shape: {df.shape}")

        # 2. Validation
        if self.validator:
            print(f"[Pipeline] Validating data using {self.validator.__name__}...")
            try:
                self.validator.validate(df)
                print("[Pipeline] Validation successful.")
            except Exception as e:
                print(f"[Pipeline] Validation failed: {e}")
                raise e
        else:
            print("[Pipeline] No validator set, skipping validation.")

        # 3. Saving
        if self.saver:
            print("[Pipeline] Saving data...")
            self.saver(df)
            print("[Pipeline] Data saved.")
        else:
            print("[Pipeline] No saver set, skipping save.")

        return df

class PipelineBuilder:
    """
    Builder for creating Pipeline instances.
    """
    def __init__(self):
        self.pipeline = Pipeline()

    def with_extractor(self, extractor_type: str, **kwargs):
        """
        Sets the extractor using the ExtractorFactory.
        """
        extractor = ExtractorFactory.get_extractor(extractor_type, **kwargs)
        self.pipeline.set_extractor(extractor)
        return self

    def with_validator(self, validator_class):
        """
        Sets the validator class.
        """
        self.pipeline.set_validator(validator_class)
        return self

    def with_saver(self, saver_func):
        """
        Sets the saver function.
        """
        self.pipeline.set_saver(saver_func)
        return self

    def build(self):
        """
        Returns the constructed Pipeline.
        """
        return self.pipeline
