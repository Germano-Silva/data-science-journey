import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import logging
import sys

# Add parent directory to path for absolute imports
sys.path.append(str(Path(__file__).parent))

import config
import utils
from config import (
    DATA_RAW_DIR, CSV_FILE_PATTERN, MD_FILE_PATTERN,
    COURSE_CATEGORIES, COLUMN_MAPPING
)
from utils import setup_logging, clean_text

logger = setup_logging()

def extract_csv_files() -> List[Dict[str, Any]]:
    """Extract data from all CSV files"""
    csv_files = list(DATA_RAW_DIR.glob(CSV_FILE_PATTERN))
    logger.info(f"Found {len(csv_files)} CSV files to process")

    all_records = []

    for csv_file in csv_files:
        try:
            logger.info(f"Processing file: {csv_file.name}")
            df = pd.read_csv(csv_file)

            # Determine file type based on filename
            filename = csv_file.name.lower()

            if "ingles - aulas" in filename:
                records = _extract_ingles_aulas(df)
            elif "modulos" in filename:
                records = _extract_modulos(df, filename)
            else:
                records = _extract_standard_csv(df, filename)

            all_records.extend(records)

        except Exception as e:
            logger.error(f"Error processing {csv_file.name}: {str(e)}")
            continue

    return all_records

def _extract_standard_csv(df: pd.DataFrame, filename: str) -> List[Dict[str, Any]]:
    """Extract data from standard CSV files"""
    records = []
    column_mapping = COLUMN_MAPPING["csv"]

    for _, row in df.iterrows():
        record = {
            "source_file": filename,
            "course_name": clean_text(row.get(column_mapping["course_name"])),
            "module": clean_text(row.get(column_mapping["module"])),
            "module_name": clean_text(row.get(column_mapping["module_name"])),
            "lesson": clean_text(row.get(column_mapping["lesson"])),
            "start_date": clean_text(row.get(column_mapping["start_date"])),
            "end_date": clean_text(row.get(column_mapping["end_date"])),
            "status": clean_text(row.get(column_mapping["status"])),
            "raw_data": row.to_dict()
        }
        records.append(record)

    return records

def _extract_ingles_aulas(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Extract data from Inglês Aulas CSV"""
    records = []
    column_mapping = COLUMN_MAPPING["ingles_aulas"]

    for _, row in df.iterrows():
        record = {
            "source_file": "Trilha Ingles - Aulas.csv",
            "course_name": clean_text(row.get(column_mapping["course_name"])),
            "module": clean_text(row.get(column_mapping["module"])),
            "lesson": clean_text(row.get(column_mapping["lesson"])),
            "start_date": clean_text(row.get(column_mapping["start_date"])),
            "end_date": clean_text(row.get(column_mapping["end_date"])),
            "status": clean_text(row.get(column_mapping["status"])),
            "raw_data": row.to_dict()
        }
        records.append(record)

    return records

def _extract_modulos(df: pd.DataFrame, filename: str) -> List[Dict[str, Any]]:
    """Extract data from Modulos CSV files"""
    records = []

    if "ingles" in filename.lower():
        # Inglês Modulos structure
        for _, row in df.iterrows():
            record = {
                "source_file": filename,
                "module_id": row.get("ID", ""),
                "module_name": clean_text(row.get("Módulo")),
                "duration_total": clean_text(row.get("Duração Total")),
                "lessons_count": clean_text(row.get("Aulas")),
                "raw_data": row.to_dict()
            }
            records.append(record)
    else:
        # Other modulos structure (Analise de Dados)
        for _, row in df.iterrows():
            record = {
                "source_file": filename,
                "course_id": row.get("ID Curso", ""),
                "course_name": clean_text(row.get("Nome do Curso")),
                "status_geral": clean_text(row.get("Status Geral")),
                "nota_minima": clean_text(row.get("Nota Mínima")),
                "tempo_prova": clean_text(row.get("Tempo de Prova")),
                "questoes": clean_text(row.get("Questões")),
                "raw_data": row.to_dict()
            }
            records.append(record)

    return records

def extract_md_files() -> List[Dict[str, Any]]:
    """Extract data from MD files"""
    md_files = list(DATA_RAW_DIR.glob(MD_FILE_PATTERN))
    logger.info(f"Found {len(md_files)} MD files to process")

    all_records = []

    for md_file in md_files:
        try:
            logger.info(f"Processing MD file: {md_file.name}")
            content = md_file.read_text(encoding='utf-8')

            if "ingles" in md_file.name.lower():
                records = _extract_ingles_md(content)
                all_records.extend(records)

        except Exception as e:
            logger.error(f"Error processing {md_file.name}: {str(e)}")
            continue

    return all_records

def _extract_ingles_md(content: str) -> List[Dict[str, Any]]:
    """Extract lesson durations from Inglês MD file"""
    import re
    from utils import parse_duration

    records = []
    current_module = None
    current_module_name = None

    # Find all module sections
    module_sections = re.findall(
        r'#### **Módulo \d+: ([^\\n]+)**.*?\\n\\| Nome do Curso \\| Módulo \\| Nome do Módulo \\| Aula \\| Duração \\| Data Início \\| Data Fim \\| Status \\|(.*?)####',
        content,
        re.DOTALL
    )

    for module_name, table_content in module_sections:
        # Extract module number from name
        module_match = re.search(r'Módulo (\d+)', module_name)
        if module_match:
            current_module = int(module_match.group(1))
            current_module_name = module_name.split(': ')[1] if ': ' in module_name else module_name

        # Extract table rows
        rows = re.findall(
            r'\\| Inglês Online \\| \d+ \\| [^\\|]+ \\| ([^\\|]+) \\| ([^\\|]+) \\|',
            table_content
        )

        for lesson_name, duration in rows:
            record = {
                "source_file": "ingles.md",
                "module": current_module,
                "module_name": current_module_name,
                "lesson": clean_text(lesson_name),
                "duration": parse_duration(duration),
                "raw_data": {
                    "lesson": lesson_name,
                    "duration": duration
                }
            }
            records.append(record)

    return records
