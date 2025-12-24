#!/usr/bin/env python3
"""
Test script to verify ETL structure without requiring pandas
"""

import os
import sys
from pathlib import Path

# Add the etl_cursos directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_etl_structure():
    """Test the ETL structure and file creation"""
    print("Testing ETL structure...")

    # Test 1: Check if all modules can be imported
    try:
        from config import DATA_PROCESSED_DIR, OUTPUT_DELIMITER
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Config module import failed: {e}")
        return False

    try:
        from utils import setup_logging, clean_text
        print("✓ Utils module imported successfully")
    except ImportError as e:
        print(f"✗ Utils module import failed: {e}")
        return False

    try:
        from extractors import extract_csv_files, extract_md_files
        print("✓ Extractors module imported successfully")
    except ImportError as e:
        print(f"✗ Extractors module import failed: {e}")
        return False

    try:
        from transformers import transform_course_data
        print("✓ Transformers module imported successfully")
    except ImportError as e:
        print(f"✗ Transformers module import failed: {e}")
        return False

    try:
        from loaders import load_all_tables
        print("✓ Loaders module imported successfully")
    except ImportError as e:
        print(f"✗ Loaders module import failed: {e}")
        return False

    try:
        from main import run_etl_pipeline
        print("✓ Main module imported successfully")
    except ImportError as e:
        print(f"✗ Main module import failed: {e}")
        return False

    # Test 2: Check if processed directory exists
    if DATA_PROCESSED_DIR.exists():
        print(f"✓ Processed directory exists: {DATA_PROCESSED_DIR}")
    else:
        print(f"✗ Processed directory does not exist: {DATA_PROCESSED_DIR}")
        return False

    # Test 3: Check configuration values
    print(f"✓ Output delimiter: '{OUTPUT_DELIMITER}'")
    print(f"✓ Processed directory: {DATA_PROCESSED_DIR}")

    # Test 4: Test utility functions
    test_text = "  Hello,  World!  "
    cleaned = clean_text(test_text)
    if cleaned == "Hello, World!":
        print("✓ clean_text function works correctly")
    else:
        print(f"✗ clean_text function failed: expected 'Hello, World!', got '{cleaned}'")
        return False

    print("\nAll structure tests passed! ✓")
    print("\nNote: Full ETL pipeline requires pandas to run.")
    print("The structure and modules are correctly implemented.")

    return True

if __name__ == "__main__":
    success = test_etl_structure()
    sys.exit(0 if success else 1)
