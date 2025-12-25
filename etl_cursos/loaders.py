import pandas as pd
from typing import Dict
import logging
import sys
from pathlib import Path

# Add parent directory to path for absolute imports
sys.path.append(str(Path(__file__).parent))

import config
import utils
from config import OUTPUT_DELIMITER, OUTPUT_ENCODING
from utils import setup_logging, generate_output_filename, save_dataframe

logger = setup_logging()

def load_all_tables(tables: Dict[str, pd.DataFrame]) -> None:
    """Load all transformed tables to CSV files"""
    logger.info("Starting data loading process...")

    # Define table names and their corresponding dataframes
    table_mapping = {
        "dim_cursos": "DIM_CURSOS",
        "dim_modulos": "DIM_MODULOS",
        "dim_aulas": "DIM_AULAS",
        "dim_status": "DIM_STATUS",
        "dim_tempo": "DIM_TEMPO",
        "fato_progresso": "FATO_PROGRESSO"
    }

    for table_name, df in tables.items():
        if table_name in table_mapping:
            output_filename = generate_output_filename(table_mapping[table_name])
            save_dataframe(df, output_filename)
            logger.info(f"Successfully loaded {table_name} with {len(df)} records")

    logger.info("Data loading completed successfully!")

def load_dim_cursos(df: pd.DataFrame) -> None:
    """Load DIM_CURSOS table"""
    filename = generate_output_filename("DIM_CURSOS")
    save_dataframe(df, filename)

def load_dim_modulos(df: pd.DataFrame) -> None:
    """Load DIM_MODULOS table"""
    filename = generate_output_filename("DIM_MODULOS")
    save_dataframe(df, filename)

def load_dim_aulas(df: pd.DataFrame) -> None:
    """Load DIM_AULAS table"""
    filename = generate_output_filename("DIM_AULAS")
    save_dataframe(df, filename)

def load_dim_status(df: pd.DataFrame) -> None:
    """Load DIM_STATUS table"""
    filename = generate_output_filename("DIM_STATUS")
    save_dataframe(df, filename)

def load_fato_progresso(df: pd.DataFrame) -> None:
    """Load FATO_PROGRESSO table"""
    filename = generate_output_filename("FATO_PROGRESSO")
    save_dataframe(df, filename)

def validate_output_data(tables: Dict[str, pd.DataFrame]) -> bool:
    """Validate the output data structure"""
    logger.info("Validating output data...")

    required_tables = ["dim_cursos", "dim_modulos", "dim_aulas", "dim_status", "dim_tempo", "fato_progresso"]

    for table_name in required_tables:
        if table_name not in tables:
            logger.error(f"Missing required table: {table_name}")
            return False

        df = tables[table_name]
        if df.empty:
            logger.error(f"Table {table_name} is empty")
            return False

        # Check for required columns
        if table_name == "dim_cursos" and "id_curso" not in df.columns:
            logger.error("DIM_CURSOS missing id_curso column")
            return False

        if table_name == "dim_modulos" and "id_modulo" not in df.columns:
            logger.error("DIM_MODULOS missing id_modulo column")
            return False

        if table_name == "dim_aulas" and "id_aula" not in df.columns:
            logger.error("DIM_AULAS missing id_aula column")
            return False

        if table_name == "dim_status" and "id_status" not in df.columns:
            logger.error("DIM_STATUS missing id_status column")
            return False

        if table_name == "dim_tempo" and "id_tempo" not in df.columns:
            logger.error("DIM_TEMPO missing id_tempo column")
            return False

        if table_name == "fato_progresso" and "id_curso" not in df.columns:
            logger.error("FATO_PROGRESSO missing required columns")
            return False

        if table_name == "fato_progresso" and "id_tempo" not in df.columns:
            logger.error("FATO_PROGRESSO missing id_tempo column")
            return False

    logger.info("Data validation passed successfully!")
    return True
