import os
import json
import argparse

def main(input_file_path, output_dir):
    # Load JSON data
    with open(input_file_path, 'r') as f:
        data = json.load(f)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over the results and create .txt files containing the message
    results = data.get('results', [])
    for index, result in enumerate(results):
        file_path = os.path.join(output_dir, f"{index}.txt")
        # Retrieve the prompt from the 'metadata' object
        prompt = result.get('extra', {}).get('metadata', {}).get('prompt', 'No prompt available')

        # Write the prompt message to the file
        with open(file_path, 'w') as f:
            f.write(prompt)
            f.write("\n\n")

        # Extract the path and the line range
        code_path = result.get('path')
        start_line = result.get('start', {}).get('line')
        end_line = result.get('end', {}).get('line')

        # Check for valid path and line numbers
        if code_path and start_line is not None and end_line is not None:
            current_dir = os.path.dirname(__file__)
            full_code_path = os.path.join(current_dir, ".", code_path)
            
            try:
                with open(full_code_path, 'r') as code_file:
                    lines = code_file.readlines()

                # Extract the relevant lines and join them
                code_snippet = ''.join(lines[start_line - 1:end_line])  # -1 because list indices start at 0

                # Write the extracted code snippet to the output file
                with open(file_path, 'a') as f:
                    f.write(code_snippet)

            except FileNotFoundError:
                # Handle the case where the file is not found
                with open(file_path, 'a') as f:
                    f.write(f"Error: File not found at path {code_path}")

    # Report the number of prompts prepared
    print(f"{len(results)} Prompts prepared successfully.")

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process JSON results and generate prompt files.")
    parser.add_argument(
        '--input_file_path',
        type=str,
        required=True,
        help="Path to the input JSON file containing results."
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help="Directory where output .txt files will be saved."
    )

    # Parse arguments
    args = parser.parse_args()

    # Call main with parsed arguments
    main(args.input_file_path, args.output_dir)