# ETL Pipeline for Course Data Processing

## Overview

This ETL (Extract, Transform, Load) pipeline processes course data from multiple CSV and Markdown files into a structured star schema data warehouse. The pipeline is designed to handle data from three main course categories:

1. **Análise de Dados e TI Aplicado a Gestão** (12 modules)
2. **Formação em Cientista de Dados** (Excel and Introduction modules)
3. **Inglês Online** (23 modules with 225 lessons)

## Project Structure

```
etl_cursos/
├── config.py              # Configuration settings
├── extractors.py          # Data extraction functions
├── transformers.py        # Data transformation functions
├── loaders.py             # Data loading functions
├── utils.py               # Utility functions
├── main.py                # Main ETL pipeline
├── test_etl_basic.py      # Basic structure tests
├── test_etl_structure.py  # Full structure tests
└── README.md              # Documentation
```

## Star Schema Design

The ETL pipeline transforms the raw data into a star schema with the following tables:

### Fact Table
- **FATO_PROGRESSO**: Central table containing course progress records with foreign keys to all dimensions

### Dimension Tables
- **DIM_CURSOS**: Course information (name, category, requirements)
- **DIM_MODULOS**: Module information (name, order, estimated duration)
- **DIM_AULAS**: Lesson information (name, individual duration, content type)
- **DIM_STATUS**: Status information (description of progress status)
- **DIM_TEMPO**: Time information (dates, semesters) - *future implementation*

## Installation

The pipeline requires Python 3.8+ and the following packages:

```bash
pip install pandas
```

## Configuration

The `config.py` file contains all configuration settings:

- **Directories**: Input and output paths
- **File Patterns**: CSV and MD file patterns
- **Output Settings**: Delimiter (`;`) and encoding (`utf-8`)
- **Course Categories**: Mapping of course categories
- **Status Mapping**: Standardization of status values
- **Column Mapping**: Mapping of column names between different file formats

## Running the Pipeline

To run the complete ETL pipeline:

```bash
cd etl_cursos
python3 main.py
```

## Pipeline Steps

1. **Extraction**: Reads all CSV and MD files from `data/raw/informacoes-cursos/`
2. **Transformation**: Converts raw data into star schema dimensional tables
3. **Validation**: Ensures data quality and schema compliance
4. **Loading**: Saves processed data to `data/processed/` as CSV files with `;` delimiter

## Data Processing Features

### Extraction
- Handles multiple CSV file formats (standard, módulos, inglês aulas)
- Parses Markdown files for additional lesson duration data
- Robust error handling for file reading

### Transformation
- Creates dimensional tables from raw data
- Maps status values to standardized format
- Extracts module numbers from module names
- Merges data from multiple sources (CSV + MD)
- Handles different file structures appropriately

### Loading
- Saves all tables as CSV files with `;` delimiter
- Uses UTF-8 encoding for international characters
- Includes logging for progress tracking
- Validates output data structure

## Testing

Two test scripts are provided:

1. **Basic Test** (no pandas required):
```bash
python3 test_etl_basic.py
```

2. **Full Test** (requires pandas):
```bash
python3 test_etl_structure.py
```

## Output Files

The pipeline generates the following CSV files in `data/processed/`:

- `DIM_CURSOS.csv` - Course dimension
- `DIM_MODULOS.csv` - Module dimension
- `DIM_AULAS.csv` - Lesson dimension
- `DIM_STATUS.csv` - Status dimension
- `FATO_PROGRESSO.csv` - Progress fact table
- `etl.log` - Processing log file

## Data Quality Features

- Text cleaning and normalization
- Duration parsing and standardization
- Status value mapping
- Error handling and logging
- Data validation

## Future Enhancements

1. Implement DIM_TEMPO dimension with proper date handling
2. Add more robust error recovery
3. Implement data quality metrics
4. Add support for incremental loading
5. Create visualization dashboards

## Troubleshooting

If you encounter issues:

1. Ensure pandas is installed: `pip install pandas`
2. Check file permissions on input directories
3. Review the log file: `data/processed/etl.log`
4. Run basic tests first: `python3 test_etl_basic.py`

## License

This project is licensed under the MIT License.
