# src/config.py
import os

# Define version
VERSION = "1.0.0"

# Define absolute paths to data directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to src directory
PROJECT_ROOT = os.path.join(BASE_DIR, "..")  # Path to project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")  # Path to data directory
VENV_DIR = os.path.join(PROJECT_ROOT, "venv")  # Path to venv directory
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")  # Path to requirements.txt
TEST_DIR = os.path.join(PROJECT_ROOT, "test")  # Path to test directory

# Specific data directories
ANALYSIS_OUTPUT_DIR = os.path.join(DATA_DIR, "analysis_output")
ANALYSIS_OUTPUT_FILE = os.path.join(ANALYSIS_OUTPUT_DIR, "results.json")
INPUT_PROMPTS_DIR = os.path.join(DATA_DIR, "input_prompts")
MODEL_INPUT_DIR = os.path.join(DATA_DIR, "model_input")
MODEL_INPUT_FILE = os.path.join(MODEL_INPUT_DIR, "input.json")
MODEL_OUTPUT_DIR = os.path.join(DATA_DIR, "model_output")
RULES_DIR = os.path.join(PROJECT_ROOT, "rules")
DIST_DIR = os.path.join(DATA_DIR, "dist")

# Test directories and files
TEST_FILES_DIR = os.path.join(PROJECT_ROOT, "test_files")  # Test files directory

TEST_RULES_DIR = os.path.join(TEST_FILES_DIR, "rules")  # Test files
TEST_PROGRAMS_DIR = os.path.join(TEST_FILES_DIR, "programs")  # Test programs

TEST_RULES_FILE = os.path.join(TEST_RULES_DIR, "test.yml")  # Test rule file
TEST_PROGRAMS_FILE = os.path.join(TEST_PROGRAMS_DIR, "Test.java")  # Test program file
