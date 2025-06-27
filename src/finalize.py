import json
import os
import argparse

def process_json_file(analysis_output_file, project_dir, model_output_dir):
    try:
        with open(analysis_output_file, 'r') as file:
            print("File opened successfully, reading content...")
            data = json.load(file)
        
        for i, result in enumerate(data['results'], 0):
            index = i
            path = result['path']
            start_line = result['start']['line']
            end_line = result['end']['line']

            print("-" * 50)
            # 2. Fetch the original code
            print("Fetching original code...")

            # Use project_dir instead of relative path calculation
            original_path = os.path.join(project_dir, path)
            original_code = None

            # Fetch file content
            with open(original_path, 'r') as file:
                original_code = file.readlines()
                print(*original_code, sep='\n')

            print("-" * 50)
            # 2. Fetch the refactored code
            print("Fetching refactored code...")
            refactored_path = os.path.abspath(os.path.join(model_output_dir, f"{index}.java"))
            refactored_code = None

            # Fetch file content
            with open(refactored_path, 'r') as file:
                refactored_code = file.readlines()
                print(*refactored_code, sep='\n')

            print("-" * 50)
            # 3. Add the refactored code in the original code
            print("Insert refactored code in the original code between start and end lines...")
        
            # 3.1 Get original indentation from the start line
            original_line = original_code[start_line - 1]
            original_indent = original_line[:len(original_line) - len(original_line.lstrip())]

            # 3.2 Apply indentation to each line of refactored code
            refactored_indented = [original_indent + line for line in refactored_code]

            # 3.3 Replace the original code lines with the indented refactored code
            modified_code = (
                original_code[:start_line - 1] 
                + refactored_indented 
                + original_code[end_line:]
            )

            print(*modified_code, sep='\n')

            # 4. Replace the original code with the modified code
            with open(original_path, 'w') as file:
                file.writelines(modified_code)

            # 5. Clean output directory TODO    
            
    except FileNotFoundError:
        print(f"Error: File not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{analysis_output_file}'.")
    except KeyError as e:
        print(f"Error: Missing expected key in JSON data - {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process JSON file with project directory")
    parser.add_argument(
        "--analysis-output-file",
        type=str,
        required=True,
        help="Absolute path to the analysis output JSON file"
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        required=True,
        help="Absolute path to the project directory"
    )
    parser.add_argument(
        "--model-output-dir",
        type=str,
        required=True,
        help="Absolute path to the model output directory"
    )

    print("Finalizing refactoring process...")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with analysis_output_file, project_dir, and model_output_dir
    process_json_file(args.analysis_output_file, args.project_dir, args.model_output_dir)