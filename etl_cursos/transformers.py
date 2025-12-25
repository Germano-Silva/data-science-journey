import pandas as pd
from typing import List, Dict, Any
import logging
import sys
from pathlib import Path

# Add parent directory to path for absolute imports
sys.path.append(str(Path(__file__).parent))

import config
import utils
from config import STATUS_MAPPING
from utils import setup_logging, extract_module_number, create_dataframe_from_records

logger = setup_logging()

def normalize_course_structure(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize course structure to fix granularity issues"""
    normalized = []

    for record in records:
        # Skip modulos records
        if "module_id" in record or "course_id" in record:
            normalized.append(record)
            continue

        course_name = record.get("course_name", "")
        module_name = record.get("module_name", "")
        lesson_name = record.get("lesson", "")
        status_desc = record.get("status", "")

        # Fix for "Análise de Dados" trilogy - treat as modules of one course
        # Check if this is from the Analise de Dados trilogy by looking at specific patterns
        is_analise_dados_topic = (
            "Conceitos e Técnicas de Análise de Dados" in course_name or
            "Ferramentas de TI para coleta" in course_name or
            "Big Data e IA na tomada" in course_name or
            "Métodos para otimização" in course_name or
            "Integração da análise de dados" in course_name or
            "Técnicas de análise financeira" in course_name or
            "Go-to-Market Engineering" in course_name or
            "Cibersegurança e proteção" in course_name or
            "Utilização de SaaS para otimização" in course_name or
            "Empresas como Sistemas" in course_name or
            "Empreendedorismo Tecnológico" in course_name or
            "Projeto Final: Aplicação" in course_name or
            course_name.startswith("1.") or
            course_name.startswith("2.") or
            course_name.startswith("3.") or
            course_name.startswith("4.") or
            course_name.startswith("5.") or
            course_name.startswith("6.") or
            course_name.startswith("7.") or
            course_name.startswith("8.") or
            course_name.startswith("9.") or
            course_name.startswith("10.") or
            course_name.startswith("11.") or
            course_name.startswith("12.")
        )

        if is_analise_dados_topic:
            # Create normalized record with course as the main course
            normalized_record = record.copy()
            normalized_record["course_name"] = "Trilha Análise de Dados e TI Aplicado a Gestão"
            normalized_record["module_name"] = course_name  # Move topic to module level
            normalized_record["lesson"] = lesson_name
            normalized_record["status"] = status_desc
            normalized.append(normalized_record)
        else:
            # For Cientista de Dados, ensure we have the correct course name
            if "Cientista de Dados" in course_name and "Introdução a Análise de Dados" in lesson_name:
                normalized_record = record.copy()
                normalized_record["course_name"] = "Formação em Cientista de Dados"
                normalized.append(normalized_record)
            elif "Cientista de Dados" in course_name and "Excel Intermediário" in lesson_name:
                normalized_record = record.copy()
                normalized_record["course_name"] = "Formação em Cientista de Dados"
                normalized.append(normalized_record)
            else:
                normalized.append(record)

    return normalized

def transform_course_data(csv_records: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    """Transform course data into dimensional tables"""
    # First normalize the course structure
    normalized_records = normalize_course_structure(csv_records)

    # Initialize dimensional tables
    dim_cursos = []
    dim_modules = []
    dim_lessons = []
    dim_status = []
    fato_progresso = []

    # Create status dimension
    status_ids = {}
    for status_desc in STATUS_MAPPING.values():
        status_id = len(dim_status) + 1
        dim_status.append({
            "id_status": status_id,
            "descricao_status": status_desc
        })
        status_ids[status_desc] = status_id

    # Process each record
    course_ids = {}
    module_ids = {}
    lesson_ids = {}

    # First pass: Create all courses from modulos records to ensure Cientista de Dados is included
    for record in normalized_records:
        if "course_id" in record:
            course_id = record["course_id"]
            course_name = record["course_name"]
            status_geral = record["status_geral"]
            nota_minima = record["nota_minima"]
            tempo_prova = record["tempo_prova"]
            questoes = record["questoes"]

            # Skip the individual modules from Análise de Dados trilogy
            # These should be treated as modules, not courses
            is_analise_dados_module = (
                course_name.startswith("1.") or
                course_name.startswith("2.") or
                course_name.startswith("3.") or
                course_name.startswith("4.") or
                course_name.startswith("5.") or
                course_name.startswith("6.") or
                course_name.startswith("7.") or
                course_name.startswith("8.") or
                course_name.startswith("9.") or
                course_name.startswith("10.") or
                course_name.startswith("11.") or
                course_name.startswith("12.")
            )

            if is_analise_dados_module:
                continue  # Skip these, they'll be handled as modules later

            # Create course entry if not exists
            if course_name not in course_ids:
                course_id_key = len(dim_cursos) + 1
                course_ids[course_name] = course_id_key

                # Determine trilha origem based on course name
                trilha_origem = "Análise de Dados e TI Aplicado a Gestão"
                if "Cientista de Dados" in course_name:
                    trilha_origem = "Formação em Cientista de Dados"

                # Ensure we have the main course name for Cientista de Dados
                if "Cientista de Dados" in course_name:
                    course_name = "Formação em Cientista de Dados"

                dim_cursos.append({
                    "id_curso": course_id_key,
                    "nome_curso": course_name,
                    "trilha_origem": trilha_origem,
                    "nota_minima": nota_minima,
                    "tempo_prova": tempo_prova,
                    "qtd_questoes": questoes
                })

    # Ensure Cientista de Dados course exists
    if "Formação em Cientista de Dados" not in course_ids:
        course_id_key = len(dim_cursos) + 1
        course_ids["Formação em Cientista de Dados"] = course_id_key
        dim_cursos.append({
            "id_curso": course_id_key,
            "nome_curso": "Formação em Cientista de Dados",
            "trilha_origem": "Formação em Cientista de Dados",
            "nota_minima": "70%",
            "tempo_prova": "30 min",
            "qtd_questoes": 10
        })

    # Process Cientista de Dados trilha.csv to create modules
    process_cientista_dados_trilha(normalized_records, course_ids, module_ids, lesson_ids, dim_cursos, dim_modules, dim_lessons, fato_progresso, status_ids)

    for record in normalized_records:
        # Handle modulos records first (from módulos CSV files)
        if "module_id" in record or "course_id" in record:
            if "module_id" in record:
                # Inglês modules
                module_id = record["module_id"]
                module_name = record["module_name"]
                duration_total = record["duration_total"]

                # Create module entry
                if module_name not in module_ids:
                    module_id_key = len(dim_modules) + 1
                    module_ids[module_name] = module_id_key
                    dim_modules.append({
                        "id_modulo": module_id_key,
                        "nome_modulo": module_name,
                        "ordem_modulo": module_id,
                        "duracao_total_estimada": duration_total
                    })
            elif "course_id" in record:
                # Analise de Dados modules - already processed in first pass
                continue

            continue

        # Handle standard course/lesson records
        course_name = record.get("course_name", "")
        module_name = record.get("module_name", "")
        lesson_name = record.get("lesson", "")
        status_desc = record.get("status", "")

        # Skip records without essential fields
        if not course_name or not lesson_name:
            continue

        # Get or create course ID
        if course_name not in course_ids:
            course_id = len(dim_cursos) + 1
            course_ids[course_name] = course_id

            # Determine trilha origem based on course name
            trilha_origem = "Análise de Dados e TI Aplicado a Gestão"
            if "Cientista de Dados" in course_name:
                trilha_origem = "Formação em Cientista de Dados"
            elif "Inglês" in course_name or course_name == "Inglês":
                trilha_origem = "Inglês Online"

            dim_cursos.append({
                "id_curso": course_id,
                "nome_curso": course_name,
                "trilha_origem": trilha_origem,
                "nota_minima": "50%",
                "tempo_prova": "30 min",
                "qtd_questoes": 10
            })

        # Get or create module ID
        module_key = f"{course_name}_{module_name}"
        if module_key not in module_ids:
            module_id = len(dim_modules) + 1
            module_ids[module_key] = module_id

            # Extract module number
            module_number = extract_module_number(module_name)

            dim_modules.append({
                "id_modulo": module_id,
                "nome_modulo": module_name,
                "ordem_modulo": module_number,
                "duracao_total_estimada": "00:00:00"
            })

        # Get or create lesson ID
        lesson_key = f"{course_name}_{module_name}_{lesson_name}"
        if lesson_key not in lesson_ids:
            lesson_id = len(dim_lessons) + 1
            lesson_ids[lesson_key] = lesson_id

            dim_lessons.append({
                "id_aula": lesson_id,
                "nome_aula": lesson_name,
                "duracao_individual": "00:00:00",
                "tipo_conteudo": "Aula"
            })

        # Create fato progresso record
        status_id = status_ids.get(status_desc, 1)

        fato_progresso.append({
            "id_curso": course_ids[course_name],
            "id_modulo": module_ids[module_key],
            "id_aula": lesson_ids[lesson_key],
            "id_status": status_id,
            "nota_final": "",
            "frequencia": ""
        })

    return {
        "dim_cursos": create_dataframe_from_records(dim_cursos),
        "dim_modulos": create_dataframe_from_records(dim_modules),
        "dim_aulas": create_dataframe_from_records(dim_lessons),
        "dim_status": create_dataframe_from_records(dim_status),
        "fato_progresso": create_dataframe_from_records(fato_progresso)
    }

def transform_modulos_data(modulos_records: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    """Transform modulos data to update dimensional tables"""
    # Separate ingles modulos from other modulos
    ingles_modulos = [r for r in modulos_records if "module_id" in r]
    curso_modulos = [r for r in modulos_records if "course_id" in r]

    # Update courses with modulos data
    course_updates = {}
    for record in curso_modulos:
        course_id = record["course_id"]
        course_updates[course_id] = {
            "status_geral": record["status_geral"],
            "nota_minima": record["nota_minima"],
            "tempo_prova": record["tempo_prova"],
            "questoes": record["questoes"]
        }

    # Update modules with ingles duration data
    module_updates = {}
    for record in ingles_modulos:
        module_id = record["module_id"]
        module_updates[module_id] = {
            "duracao_total_estimada": record["duration_total"]
        }

    return {
        "course_updates": course_updates,
        "module_updates": module_updates
    }

def process_cientista_dados_trilha(csv_records: List[Dict[str, Any]], course_ids: Dict[str, int], module_ids: Dict[str, int], lesson_ids: Dict[str, int], dim_cursos: List[Dict[str, Any]], dim_modules: List[Dict[str, Any]], dim_lessons: List[Dict[str, Any]], fato_progresso: List[Dict[str, Any]], status_ids: Dict[str, int]) -> None:
    """Process Cientista de Dados trilha.csv file to create modules and lessons"""
    # Find records from the trilha.csv file
    trilha_records = [r for r in csv_records if "source_file" in r and "trilha.csv" in r.get("source_file", "").lower()]

    for record in trilha_records:
        if "course_id" in record:
            # This is a module definition from the trilha.csv
            course_id = record["course_id"]
            course_name = record["course_name"]
            module_name = record.get("module_name", "")
            status_geral = record.get("status_geral", "")

            # Ensure the course exists
            if course_name not in course_ids:
                # If course doesn't exist, use the main course name
                course_name = "Formação em Cientista de Dados"
                if course_name not in course_ids:
                    continue

            # Create module if it doesn't exist
            module_key = f"{course_name}_{module_name}"
            if module_key not in module_ids:
                module_id = len(dim_modules) + 1
                module_ids[module_key] = module_id

                # Extract module number from the course_id (which is the module number in trilha.csv)
                module_number = int(course_id)

                dim_modules.append({
                    "id_modulo": module_id,
                    "nome_modulo": module_name,
                    "ordem_modulo": module_number,
                    "duracao_total_estimada": "00:00:00"
                })

            # Create a fato progresso record for the module
            status_id = status_ids.get(status_geral, 1)
            fato_progresso.append({
                "id_curso": course_ids[course_name],
                "id_modulo": module_ids[module_key],
                "id_aula": 0,  # No specific lesson for module-level status
                "id_status": status_id,
                "nota_final": "",
                "frequencia": ""
            })

def transform_ingles_durations(md_records: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    """Transform ingles lesson durations from MD file"""
    lesson_durations = {}

    for record in md_records:
        module = record["module"]
        lesson = record["lesson"]
        duration = record["duration"]

        # Create a key for the lesson
        lesson_key = f"module_{module}_{lesson}"
        lesson_durations[lesson_key] = duration

    return {"lesson_durations": lesson_durations}

def merge_all_data(
    course_data: Dict[str, pd.DataFrame],
    modulos_data: Dict[str, Any],
    ingles_durations: Dict[str, Any]
) -> Dict[str, pd.DataFrame]:
    """Merge all transformed data"""
    # Start with course data
    result = course_data.copy()

    # Update courses with modulos data
    if "course_updates" in modulos_data:
        course_updates = modulos_data["course_updates"]
        dim_cursos = result["dim_cursos"]

        for _, row in dim_cursos.iterrows():
            course_id = row["id_curso"]
            if str(course_id) in course_updates:
                update = course_updates[str(course_id)]
                for col, value in update.items():
                    if col in dim_cursos.columns:
                        dim_cursos.loc[dim_cursos["id_curso"] == course_id, col] = value

    # Update modules with modulos data
    if "module_updates" in modulos_data:
        module_updates = modulos_data["module_updates"]
        dim_modulos = result["dim_modulos"]

        for _, row in dim_modulos.iterrows():
            module_id = row["id_modulo"]
            if str(module_id) in module_updates:
                update = module_updates[str(module_id)]
                for col, value in update.items():
                    if col in dim_modulos.columns:
                        dim_modulos.loc[dim_modulos["id_modulo"] == module_id, col] = value

    # Update lesson durations from MD file
    if "lesson_durations" in ingles_durations:
        lesson_durations = ingles_durations["lesson_durations"]
        dim_aulas = result["dim_aulas"]

        for _, row in dim_aulas.iterrows():
            lesson_id = row["id_aula"]
            lesson_name = row["nome_aula"]

            # Try to find matching duration
            for key, duration in lesson_durations.items():
                if lesson_name in key:
                    dim_aulas.loc[dim_aulas["id_aula"] == lesson_id, "duracao_individual"] = duration
                    break

    return result
