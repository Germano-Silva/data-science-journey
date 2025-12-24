#!/usr/bin/env python3
"""
Basic test script to verify ETL structure without importing pandas-dependent modules
"""

import os
import sys
from pathlib import Path

# Add the etl_cursos directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_etl_basic_structure():
    """Test the basic ETL structure"""
    print("Testing basic ETL structure...")

    # Test 1: Check if config module can be imported
    try:
        from config import DATA_PROCESSED_DIR, OUTPUT_DELIMITER, COURSE_CATEGORIES
        print("✓ Config module imported successfully")
        print(f"  - Processed directory: {DATA_PROCESSED_DIR}")
        print(f"  - Output delimiter: '{OUTPUT_DELIMITER}'")
        print(f"  - Course categories: {list(COURSE_CATEGORIES.keys())}")
    except ImportError as e:
        print(f"✗ Config module import failed: {e}")
        return False

    # Test 2: Check if processed directory exists
    if DATA_PROCESSED_DIR.exists():
        print(f"✓ Processed directory exists: {DATA_PROCESSED_DIR}")
    else:
        print(f"✗ Processed directory does not exist: {DATA_PROCESSED_DIR}")
        return False

    # Test 3: Check file structure
    expected_files = [
        "config.py",
        "utils.py",
        "extractors.py",
        "transformers.py",
        "loaders.py",
        "main.py",
        "test_etl_structure.py",
        "test_etl_basic.py"
    ]

    for file in expected_files:
        file_path = Path(__file__).parent / file
        if file_path.exists():
            print(f"✓ File exists: {file}")
        else:
            print(f"✗ File missing: {file}")
            return False

    # Test 4: Check if main.py has the expected structure
    try:
        with open(Path(__file__).parent / "main.py", "r") as f:
            content = f.read()
            if "run_etl_pipeline" in content:
                print("✓ Main module has run_etl_pipeline function")
            else:
                print("✗ Main module missing run_etl_pipeline function")
                return False
    except Exception as e:
        print(f"✗ Error reading main.py: {e}")
        return False

    print("\nBasic structure tests passed! ✓")
    print("\nETL Implementation Summary:")
    print("- Config: Centralized configuration with paths and settings")
    print("- Extractors: Functions to read CSV and MD files")
    print("- Transformers: Functions to transform data into star schema")
    print("- Loaders: Functions to save data to CSV files")
    print("- Main: Orchestrates the complete ETL pipeline")
    print("- Utils: Helper functions for text processing and logging")

    print("\nThe ETL pipeline is ready to run once pandas is installed.")
    print("To run the full pipeline: python3 main.py")

    return True

if __name__ == "__main__":
    success = test_etl_basic_structure()
    sys.exit(0 if success else 1)
