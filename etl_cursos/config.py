# ETL Configuration
import os
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent
DATA_RAW_DIR = BASE_DIR.parent / "data" / "raw" / "informacoes-cursos"
DATA_PROCESSED_DIR = BASE_DIR.parent / "data" / "processed"
DATA_PROCESSED_DIR.mkdir(exist_ok=True)

# File patterns
CSV_FILE_PATTERN = "*.csv"
MD_FILE_PATTERN = "*.md"

# Output settings
OUTPUT_DELIMITER = ";"
OUTPUT_ENCODING = "utf-8"

# Course categories
COURSE_CATEGORIES = {
    "analise_dados": "Trilha Analise de Dados e TI Aplicado a Gestao",
    "cientista_dados": "Trilha Formação em Cientista de Dados",
    "ingles": "Trilha Ingles"
}

# Status mapping
STATUS_MAPPING = {
    "Aprovado": "Aprovado",
    "Em andamento": "Em andamento",
    "Aguardando início": "Aguardando início",
    "Concluído": "Concluído",
    "Indisponível": "Indisponível",
    "N/D": "Não disponível"
}

# Column names mapping
COLUMN_MAPPING = {
    "csv": {
        "course_name": "Nome do Curso",
        "module": "Módulo",
        "module_name": "Nome do Módulo",
        "lesson": "Aulas (Tópicos/Conteúdo)",
        "start_date": "Data Início",
        "end_date": "Data Fim",
        "status": "Status"
    },
    "ingles_aulas": {
        "course_name": "Nome do Curso",
        "module": "Módulos",
        "lesson": "Aulas",
        "start_date": "Data de Início",
        "end_date": "Data de Fim",
        "status": "Status"
    }
}
