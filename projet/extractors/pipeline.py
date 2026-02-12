"""
Pipeline module.

Contains:
- Pipeline class for executing Extract -> Validate -> Save flow.
- PipelineBuilder class for constructing pipeline instances.
"""

# --- Standard / Third-party imports ---
from typing import Callable, Optional
import pandas as pd

# --- Local imports ---
from .extractor_factory import ExtractorFactory
from .decorators import log_execution_time


class Pipeline:
    """
    Represents a data processing pipeline.
    Handles extraction, validation, and saving.
    """

    def __init__(self) -> None:
        """Initialize an empty pipeline."""
        self.extractor = None
        self.validator = None
        self.saver: Optional[Callable[[pd.DataFrame], None]] = None

    def set_extractor(self, extractor) -> None:
        """Set the extractor instance."""
        self.extractor = extractor

    def set_validator(self, validator) -> None:
        """Set the validator class."""
        self.validator = validator

    def set_saver(self, saver: Callable[[pd.DataFrame], None]) -> None:
        """Set the saver function."""
        self.saver = saver

    @log_execution_time
    def run(self) -> pd.DataFrame:
        """
        Execute the pipeline:
        1. Extract
        2. Validate
        3. Save
        """
        print("[Pipeline] Starting Pipeline...")

        # 1️⃣ Extraction
        if not self.extractor:
            raise ValueError("No extractor set in pipeline!")

        print(
            "[Pipeline] Extracting data using "
            f"{self.extractor.__class__.__name__}..."
        )

        try:
            raw_data = self.extractor.extract()
            df = self.extractor.to_dataframe(raw_data)
        except (ValueError, RuntimeError) as error:
            print(f"[Pipeline] Extraction failed: {error}")
            return pd.DataFrame()
        except Exception as error:  # pylint: disable=broad-exception-caught
            print(f"[Pipeline] Unexpected extraction error: {error}")
            return pd.DataFrame()

        print(
            "[Pipeline] Extraction complete. "
            f"DataFrame shape: {df.shape}"
        )

        # 2️⃣ Validation
        if self.validator:
            validator_name = getattr(
                self.validator,
                "__name__",
                self.validator.__class__.__name__,
            )

            print(
                "[Pipeline] Validating data using "
                f"{validator_name}..."
            )

            try:
                self.validator.validate(df)
                print("[Pipeline] Validation successful.")
            except ValueError as error:
                print(f"[Pipeline] Validation failed: {error}")
                raise

        else:
            print("[Pipeline] No validator set, skipping validation.")

        # 3️⃣ Saving
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
    Allows fluent configuration.
    """

    def __init__(self) -> None:
        """Initialize a new builder with an empty pipeline."""
        self.pipeline = Pipeline()

    def with_extractor(self, extractor_type: str, **kwargs) -> "PipelineBuilder":
        """
        Set extractor using ExtractorFactory.
        """
        extractor = ExtractorFactory.get_extractor(
            extractor_type,
            **kwargs,
        )
        self.pipeline.set_extractor(extractor)
        return self

    def with_validator(self, validator_class) -> "PipelineBuilder":
        """
        Set validator class.
        """
        self.pipeline.set_validator(validator_class)
        return self

    def with_saver(
        self,
        saver_func: Callable[[pd.DataFrame], None],
    ) -> "PipelineBuilder":
        """
        Set saver function.
        """
        self.pipeline.set_saver(saver_func)
        return self

    def build(self) -> Pipeline:
        """
        Return the configured Pipeline instance.
        """
        return self.pipeline
