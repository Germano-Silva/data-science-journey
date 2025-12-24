#!/usr/bin/env python3
"""
ETL Pipeline Runner

This script sets up the Python path correctly and runs the ETL pipeline.
"""

import sys
import os
from pathlib import Path

# Add the etl_cursos directory to the Python path
etl_dir = Path(__file__).parent
sys.path.insert(0, str(etl_dir))

# Now import the main module
from main import main

if __name__ == "__main__":
    sys.exit(main())
