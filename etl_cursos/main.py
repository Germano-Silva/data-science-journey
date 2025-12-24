#!/usr/bin/env python3
"""
ETL Pipeline for Course Data Processing

This script extracts, transforms, and loads course data from multiple CSV and MD files
into a star schema data warehouse structure.
"""

import logging
from typing import Dict
import pandas as pd
import sys
from pathlib import Path

# Add the etl_cursos directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_PROCESSED_DIR
from extractors import extract_csv_files, extract_md_files
from transformers import (
    transform_course_data,
    transform_modulos_data,
    transform_ingles_durations,
    merge_all_data
)
from loaders import load_all_tables, validate_output_data
from utils import setup_logging

def run_etl_pipeline() -> None:
    """Run the complete ETL pipeline"""
    logger = setup_logging()
    logger.info("Starting ETL pipeline...")

    try:
        # Step 1: Extraction
        logger.info("Step 1/4: Extracting data from source files...")

        csv_records = extract_csv_files()
        md_records = extract_md_files()

        logger.info(f"Extracted {len(csv_records)} records from CSV files")
        logger.info(f"Extracted {len(md_records)} records from MD files")

        # Step 2: Transformation
        logger.info("Step 2/4: Transforming data...")

        # Transform course data
        course_data = transform_course_data(csv_records)
        logger.info("Transformed course data into dimensional tables")

        # Transform modulos data
        modulos_data = transform_modulos_data(csv_records)
        logger.info("Transformed modulos data")

        # Transform ingles durations
        ingles_durations = transform_ingles_durations(md_records)
        logger.info("Transformed ingles lesson durations")

        # Merge all data
        final_data = merge_all_data(course_data, modulos_data, ingles_durations)
        logger.info("Merged all transformed data")

        # Step 3: Validation
        logger.info("Step 3/4: Validating transformed data...")

        if not validate_output_data(final_data):
            logger.error("Data validation failed. Aborting ETL process.")
            return

        # Step 4: Loading
        logger.info("Step 4/4: Loading data to output files...")

        load_all_tables(final_data)

        logger.info("ETL pipeline completed successfully!")
        logger.info("Summary:")
        for table_name, df in final_data.items():
            logger.info(f"  {table_name}: {len(df)} records")

    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}", exc_info=True)
        raise

def main() -> None:
    """Main entry point"""
    try:
        run_etl_pipeline()
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Fatal error in ETL pipeline: {str(e)}", exc_info=True)
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
