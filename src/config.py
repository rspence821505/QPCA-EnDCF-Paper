"""
Configuration management for the project.
"""

from pathlib import Path
import yaml


# Find project root dynamically
# This file is in src/config.py, so project root is one level up
PROJECT_ROOT = Path(__file__).parent.parent


EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
PAPERUQ_FIGURES_DIR = PROJECT_ROOT / "paper" / "figures"
PAPERUQ_TABLES_DIR = PROJECT_ROOT / "paper" / "tables"
PAPERUQ_DATA_DIR = PROJECT_ROOT / "paper" / "data"
PAPER_FIGURES_DIR = PROJECT_ROOT / "paper" / "figures"
PAPER_TABLES_DIR = PROJECT_ROOT / "paper" / "tables"
PAPER_DATA_DIR = PROJECT_ROOT / "paper" / "data"
BASELINE_EXPERIMENT_DIR = EXPERIMENTS_DIR / "baseline"
BASELINE_RESULTS_DIR = PROJECT_ROOT / "results" / "baseline"
DIAGNOSTICS_EXPERIMENT_DIR = EXPERIMENTS_DIR / "diagnostics"
DIAGNOSTICS_RESULTS_DIR = PROJECT_ROOT / "results" / "diagnostics"
EXTENDED_MODELS_EXPERIMENT_DIR = EXPERIMENTS_DIR / "extended_models"
EXTENDED_MODELS_RESULTS_DIR = PROJECT_ROOT / "results" / "extended_models"
SENSITIVITY_EXPERIMENT_DIR = EXPERIMENTS_DIR / "sensitivity_analysis"
SENSITIVITY_RESULTS_DIR = PROJECT_ROOT / "results" / "sensitivity"

CONFIGS_DIR = PROJECT_ROOT / "configs"
