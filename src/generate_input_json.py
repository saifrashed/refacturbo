"""
A file that generates the input json file for the program. The input of the
program is the mode and the prompts.
"""

import json
import argparse
import os
import copy

def generate_input_json(prompts_dir, json_export_dir):
    """
    Generates the input json file for the program.
    Args:
        prompts_dir: The directory containing the prompt files.
        json_export_dir: The directory where the input.json file will be saved.
    """
    prompts = []

    for filename in os.listdir(prompts_dir):
        with open(os.path.join(prompts_dir, filename), "r") as f:
            prompt = f.read()
            prompt = prompt.replace("\"", "\\\"")
            prompts.append(prompt)
            f.close()

    input_json = {
        "prompts": prompts
    }

    # Ensure the export directory exists
    os.makedirs(json_export_dir, exist_ok=True)

    # Save input.json in the specified export directory
    output_path = os.path.join(json_export_dir, "input.json")
    with open(output_path, "w") as f:
        json.dump(input_json, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts_dir", help="The directory of the prompts.", required=True)
    parser.add_argument("--json_export_dir", help="The directory to save the input.json file.", required=True)
    args = parser.parse_args()

    generate_input_json(args.prompts_dir, args.json_export_dir)