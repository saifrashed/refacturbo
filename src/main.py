#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import platform


import os

def delete_files_in_directory(path):
    """
    Recursively delete all files in the specified directory and its subdirectories.
    Directories themselves are not deleted.
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            try:
                print(f"Deleting file: {item_path}")
                os.remove(item_path)  # Delete the file
            except OSError as e:
                print(f"Error deleting file {item_path}: {e}")
        elif os.path.isdir(item_path):
            # Recursively process subdirectories
            delete_files_in_directory(item_path)


def run_command(command, cwd=None):
    """Helper function to run shell commands."""
    try:
        if isinstance(command, list):
            subprocess.run(command, check=True, cwd=cwd)
        else:
            subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Command or file not found: {e}")
        sys.exit(1)

def get_python():
    """Get the path to the Python executable, preferring virtual environment if active."""
    if os.getenv("VIRTUAL_ENV"):
        # Virtual environment is active
        python_executable = os.path.join(os.getenv("VIRTUAL_ENV"), "bin", "python3")
        if not os.path.exists(python_executable):
            print(f"Python executable not found in virtual environment at {python_executable}.")
            sys.exit(1)
        return python_executable
    # Fallback to system Python
    python_executable = sys.executable
    if not python_executable or not os.path.exists(python_executable):
        print("System Python executable not found. Ensure Python is installed and accessible.")
        sys.exit(1)
    return python_executable

def install_requirements(python_path, requirements_file):
    """Install dependencies from requirements.txt using the appropriate Python."""
    if not os.path.exists(requirements_file):
        print(f"requirements.txt not found. Please create it with your dependencies.")
        sys.exit(1)
    if os.getenv("VIRTUAL_ENV"):
        print(f"Installing dependencies from requirements.txt into virtual environment ({os.getenv('VIRTUAL_ENV')})...")
    else:
        print("Installing dependencies from requirements.txt (using system Python)...")
        print("Warning: This installs packages system-wide. Consider using a virtual environment for isolation.")
    cmd = [python_path, "-m", "pip", "install", "-r", requirements_file, "--quiet"]
    run_command(cmd)
    
def check_semgrep():
    """Check if semgrep is installed and available in the system environment."""
    try:
        subprocess.run(["semgrep", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("semgrep is not installed or not found. Install it with `pip install semgrep` or ensure it's in your PATH.")
        sys.exit(1)

def step_1(python_path, project_dir, rules_dir, analysis_output_file):
    """Run semgrep."""
    check_semgrep()
    cmd = f"semgrep --config '{rules_dir}' '{project_dir}' --output '{analysis_output_file}' --json"
    run_command(cmd)

def step_2(python_path, project_dir, base_dir, analysis_output_file, input_prompts_dir):
    """Run analysis.py."""
    cmd = [python_path, os.path.join(base_dir, "analysis.py"), "--input_file_path", analysis_output_file, "--output_dir", input_prompts_dir]
    run_command(cmd)

def step_3(python_path, project_dir, base_dir, input_prompts_dir, model_input_dir):
    """Generate input.json."""
    cmd = [python_path, os.path.join(base_dir, "generate_input_json.py"), "--prompts_dir", input_prompts_dir, "--json_export_dir", model_input_dir]
    run_command(cmd)

def step_4(python_path, project_dir, base_dir, model_input_file, model_output_dir):
    """Generate output.json."""
    cmd = [python_path, os.path.join(base_dir, "processing.py"), "--input_file", model_input_file, "--output_dir", model_output_dir]
    run_command(cmd)

def step_5(python_path, project_dir, base_dir, analysis_output_file, model_output_dir):
    """Finalize and write new code."""
    cmd = [
        python_path,
        os.path.join(base_dir, "finalize.py"),
        "--analysis-output-file", analysis_output_file,
        "--project-dir", project_dir,
        "--model-output-dir", model_output_dir
    ]
    run_command(cmd)

def run_tests(python_path, test_dir):
    """Run all unit tests in the tests directory."""
    if not os.path.exists(test_dir):
        print(f"Test directory {test_dir} does not exist. Please create it and add test files.")
        sys.exit(1)
    
    print("Running unit tests...")
    cmd = [python_path, "-m", "unittest", "discover", "-s", test_dir, "-p", "unit.py"]
    try:
        subprocess.run(cmd, check=True)
        print("All tests completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

    print("Running integration tests...")
    cmd = [python_path, "-m", "unittest", "discover", "-s", test_dir, "-p", "integration.py"]
    try:
        subprocess.run(cmd, check=True)
        print("All tests completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        sys.exit(1)    

def main():
    # Import constants here to avoid top-level import
    from config import (
        VERSION,
        BASE_DIR,
        PROJECT_ROOT,
        DATA_DIR,
        REQUIREMENTS_FILE,
        TEST_DIR,
        ANALYSIS_OUTPUT_DIR,
        ANALYSIS_OUTPUT_FILE,
        INPUT_PROMPTS_DIR,
        MODEL_INPUT_DIR,
        MODEL_INPUT_FILE,
        MODEL_OUTPUT_DIR,
        RULES_DIR,
        DIST_DIR
    )

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Refacturbo to detect and refactor green anti-patterns."
    )
    parser.add_argument("--version", action="store_true", help="Show version number and exit.")
    parser.add_argument("--install", action="store_true", help="Install dependencies before running the pipeline.")
    parser.add_argument("--refactor", type=str, default=None, help="Specify the project directory (defaults to current directory).")
    parser.add_argument("--test", action="store_true", help="Run unit tests from the tests directory.")

    args = parser.parse_args()

    # Handle --version
    if args.version:
        print(f"Refacturbo version: {VERSION}")
        sys.exit(0)

    # Get Python executable (virtual environment or system)
    python_path = get_python()

    # Install requirements
    if args.install:
        install_requirements(python_path, REQUIREMENTS_FILE)

    # Run tests
    if args.test:
        run_tests(python_path, TEST_DIR)

    # Analyze and refactor code
    if args.refactor is not None:
        # Use absolute path of the project directory
        project_dir = os.path.abspath(args.refactor)
        if not os.path.exists(project_dir):
            print(f"Project directory {project_dir} does not exist.")
            sys.exit(1)

        delete_files_in_directory(DATA_DIR)

        # Define steps with project_dir and constants passed
        steps = [
            lambda: step_1(python_path, project_dir, RULES_DIR, ANALYSIS_OUTPUT_FILE),
            lambda: step_2(python_path, project_dir, BASE_DIR, ANALYSIS_OUTPUT_FILE, INPUT_PROMPTS_DIR),
            lambda: step_3(python_path, project_dir, BASE_DIR, INPUT_PROMPTS_DIR, MODEL_INPUT_DIR),
            lambda: step_4(python_path, project_dir, BASE_DIR, MODEL_INPUT_FILE, MODEL_OUTPUT_DIR),
            lambda: step_5(python_path, project_dir, BASE_DIR, ANALYSIS_OUTPUT_FILE, MODEL_OUTPUT_DIR)
        ]

        # Run all steps
        print("Running all steps...")
        for i, step_func in enumerate(steps, 1):
            print(f"Executing Step {i}...")
            step_func()
        print("All steps completed.")

if __name__ == "__main__":
    main()