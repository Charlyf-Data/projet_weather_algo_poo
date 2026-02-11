import sys
import os
import pandas as pd

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from projet.pipeline import PipelineBuilder
from projet.validators.dataframe_validator import DataFrameValidator

def dummy_saver(df: pd.DataFrame):
    """A dummy saver function for testing."""
    print(f"   [Saver] Saving {len(df)} rows to dummy storage.")

def test_builder():
    print("Testing PipelineBuilder...")

    # Example 1: CSV Pipeline
    print("\n--- Test 1: CSV Pipeline ---")
    try:
        # Create a dummy CSV file for testing
        with open("test_pipeline.csv", "w") as f:
            f.write("col1,col2\n1,2\n3,4")

        pipeline = (
            PipelineBuilder()
            .with_extractor("csv", chemin_fichier="test_pipeline.csv")
            .with_saver(dummy_saver)
            .build()
        )
        pipeline.run()
        print("[OK] CSV Pipeline ran successfully")
    except Exception as e:
        print(f"[FAIL] CSV Pipeline failed: {e}")
    finally:
        if os.path.exists("test_pipeline.csv"):
            os.remove("test_pipeline.csv")

    # Example 2: Meteo Toulouse Pipeline (with Validation)
    print("\n--- Test 2: Meteo Toulouse Pipeline ---")
    try:
        # We need a valid station. Let's try 'marengo'.
        pipeline = (
            PipelineBuilder()
            .with_extractor("meteo_toulouse", station="marengo")
            .with_validator(DataFrameValidator)
            .with_saver(dummy_saver)
            .build()
        )
        # Note: This might fail if the API is down or station is invalid, 
        # but the building process should work.
        # We'll catch the run error but verify the build.
        print("[OK] Pipeline built successfully")
        
        # Uncomment to actually run (might take time/fail on network)
        # pipeline.run() 
        
    except Exception as e:
        print(f"[FAIL] Meteo Toulouse Pipeline build failed: {e}")

if __name__ == "__main__":
    test_builder()
