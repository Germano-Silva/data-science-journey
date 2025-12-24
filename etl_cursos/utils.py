import logging
import re
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for absolute imports
sys.path.append(str(Path(__file__).parent))

import config
from config import DATA_PROCESSED_DIR, OUTPUT_DELIMITER, OUTPUT_ENCODING

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_PROCESSED_DIR / 'etl.log'),
        logging.StreamHandler()
    ]
)

def setup_logging() -> logging.Logger:
    """Setup and return logger instance"""
    return logging.getLogger('etl_cursos')

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text or pd.isna(text):
        return ""
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces
    return text

def parse_duration(duration_str: str) -> str:
    """Parse duration string to standardized format"""
    if not duration_str or pd.isna(duration_str):
        return "00:00:00"

    duration_str = str(duration_str).strip()
    if duration_str == "N/D" or duration_str.lower() == "n/d":
        return "00:00:00"

    # Handle formats like "06h:45m" or "00h:43m"
    if re.match(r'^\d+h:\d+m$', duration_str):
        hours, minutes = duration_str.split(':')
        hours = hours.replace('h', '')
        minutes = minutes.replace('m', '')
        return f"{hours.zfill(2)}:{minutes.zfill(2)}:00"

    return duration_str

def generate_output_filename(table_name: str) -> Path:
    """Generate output file path"""
    return DATA_PROCESSED_DIR / f"{table_name}.csv"

def save_dataframe(df: pd.DataFrame, filename: Path) -> None:
    """Save dataframe to CSV with proper formatting"""
    df.to_csv(
        filename,
        sep=OUTPUT_DELIMITER,
        encoding=OUTPUT_ENCODING,
        index=False
    )
    logging.info(f"Saved {len(df)} records to {filename}")

def extract_module_number(module_name: str) -> int:
    """Extract module number from module name"""
    if not module_name or pd.isna(module_name):
        return 1

    module_name = str(module_name)
    # Look for patterns like "Módulo 1", "Module 1", etc.
    match = re.search(r'(\d+)', module_name)
    if match:
        return int(match.group(1))
    return 1

def create_dataframe_from_records(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create dataframe from list of records"""
    if not records:
        return pd.DataFrame()

    # Convert all records to have the same keys
    all_keys = set()
    for record in records:
        all_keys.update(record.keys())

    normalized_records = []
    for record in records:
        normalized_record = {key: record.get(key, None) for key in all_keys}
        normalized_records.append(normalized_record)

    return pd.DataFrame(normalized_records)
