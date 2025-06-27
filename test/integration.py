#!/usr/bin/env python3
import unittest
import os
from helpers import delete_files_in_directory

from src.main import step_1, step_2, step_3, step_4, step_5, run_command, check_semgrep, get_python, install_requirements

from helpers import delete_files_in_directory

from src.config import (  # Import constants from config.py
    VERSION,
    BASE_DIR,
    PROJECT_ROOT,
    DATA_DIR,
    VENV_DIR,
    REQUIREMENTS_FILE,
    TEST_DIR,
    ANALYSIS_OUTPUT_DIR,
    ANALYSIS_OUTPUT_FILE,
    INPUT_PROMPTS_DIR,
    MODEL_INPUT_DIR,
    MODEL_INPUT_FILE,
    MODEL_OUTPUT_DIR,
    RULES_DIR,
    DIST_DIR,
    TEST_RULES_DIR,
    TEST_PROGRAMS_DIR,
    TEST_PROGRAMS_FILE
)


# AAA: Arrange, Act, Assert
class IntegrationTest(unittest.TestCase):
    python_path = None 
    program_content = None 

    @classmethod
    def setUpClass(cls): # Save the original content of the test program file
        """Run once before all tests in the class."""
        cls.python_path = get_python()
        install_requirements(cls.python_path, REQUIREMENTS_FILE)

        try:
            with open(TEST_PROGRAMS_FILE, 'r') as f:
                cls.program_content = f.read()
            print(f"Saved contents of {TEST_PROGRAMS_FILE}")
        except FileNotFoundError:
            print(f"Error: {TEST_PROGRAMS_FILE} not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading {TEST_PROGRAMS_FILE}: {e}")
            sys.exit(1)

    @classmethod
    def tearDownClass(cls): # Restore the original content of the test program file
        """Run once after all tests in the class."""
        delete_files_in_directory(DATA_DIR)
        try:
            with open(TEST_PROGRAMS_FILE, 'w') as f:
                f.write(cls.program_content)
            print(f"Restored contents of {TEST_PROGRAMS_FILE}")
        except Exception as e:
            print(f"Error writing to {TEST_PROGRAMS_FILE}: {e}")
            sys.exit(1)


    def setUp(self):
        """Run before each test method."""

    def tearDown(self):
        """Run after each test method."""

    # Example test case (add your test cases here)
    def test_step_1_to_5(self):
        """Test case to verify 'Hello, World!' in original code and 'Refactored' after steps."""
        # Arrange: Verify original content has "Hello, World!"
        with open(TEST_PROGRAMS_FILE, 'r') as f:
            original_content = f.read()
        self.assertIn("Hello, World!", original_content, "Original code does not contain 'Hello, World!'")

        # Act: Run all steps
        steps = [
            lambda: step_1(self.python_path, TEST_PROGRAMS_DIR, TEST_RULES_DIR, ANALYSIS_OUTPUT_FILE),
            lambda: step_2(self.python_path, TEST_PROGRAMS_DIR, BASE_DIR, ANALYSIS_OUTPUT_FILE, INPUT_PROMPTS_DIR),
            lambda: step_3(self.python_path, TEST_PROGRAMS_DIR, BASE_DIR, INPUT_PROMPTS_DIR, MODEL_INPUT_DIR),
            lambda: step_4(self.python_path, TEST_PROGRAMS_DIR, BASE_DIR, MODEL_INPUT_FILE, MODEL_OUTPUT_DIR),
            lambda: step_5(self.python_path, TEST_PROGRAMS_DIR, BASE_DIR, ANALYSIS_OUTPUT_FILE, MODEL_OUTPUT_DIR)
        ]

        for i, step_func in enumerate(steps, 1):
            step_func()

        # Assert: Check for "Refactored" in the modified file
        with open(TEST_PROGRAMS_FILE, 'r') as f:
            modified_content = f.read()
        self.assertIn("Refactored", modified_content, "Modified code does not contain 'Refactored'")
    
